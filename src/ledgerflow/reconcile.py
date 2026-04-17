from .db import connect


def reconcile_import(db_path, import_id: int, tolerance: float = 0.01):
    with connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT COALESCE(SUM(gross_pl),0), COALESCE(SUM(commissions_fees),0), COALESCE(SUM(net_pl),0) FROM broker_trades WHERE import_id=?",
            (import_id,),
        )
        computed_gross, computed_fees, computed_net = map(float, cur.fetchone())

        cur.execute(
            "SELECT statement_gross_pl, statement_fees, statement_net_pl FROM broker_statement_totals WHERE import_id=?",
            (import_id,),
        )
        stmt = cur.fetchone()
        stmt_gross, stmt_fees, stmt_net = stmt if stmt else (None, None, None)

        notes = []
        deltas = {"gross": None, "fees": None, "net": None}

        anchors_present = all(v is not None for v in (stmt_gross, stmt_fees, stmt_net))
        if anchors_present:
            deltas["gross"] = computed_gross - float(stmt_gross)
            deltas["fees"] = computed_fees - float(stmt_fees)
            deltas["net"] = computed_net - float(stmt_net)
            if all(abs(v) <= tolerance for v in deltas.values()):
                status = "GREEN"
            else:
                status = "RED"
                notes.append(
                    f"Mismatch beyond tolerance={tolerance}: gross={deltas['gross']:.4f}, fees={deltas['fees']:.4f}, net={deltas['net']:.4f}"
                )
        else:
            status = "YELLOW"
            missing = [n for n, v in [("statement_gross_pl", stmt_gross), ("statement_fees", stmt_fees), ("statement_net_pl", stmt_net)] if v is None]
            notes.append(f"Missing statement anchors: {', '.join(missing)}")

        cur.execute("DELETE FROM reconciliation WHERE import_id=?", (import_id,))
        cur.execute(
            """
            INSERT INTO reconciliation(import_id, status, computed_gross_pl, computed_fees, computed_net_pl, delta_gross_pl, delta_fees, delta_net_pl, notes)
            VALUES (?,?,?,?,?,?,?,?,?)
            """,
            (
                import_id,
                status,
                computed_gross,
                computed_fees,
                computed_net,
                deltas["gross"],
                deltas["fees"],
                deltas["net"],
                " | ".join(notes),
            ),
        )
        conn.commit()
        return status
