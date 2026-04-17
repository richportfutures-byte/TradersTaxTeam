from pathlib import Path
import hashlib
import json
import re

from .db import connect
from .parse_broker_csv import parse_csv

STATEMENT_MONTH_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


class DuplicateImportError(ValueError):
    """Raised when the same broker CSV file is imported more than once."""


class InvalidStatementMonthError(ValueError):
    """Raised when the statement month is not in YYYY-MM format."""


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_statement_month(statement_month: str) -> str:
    value = str(statement_month).strip()
    if not STATEMENT_MONTH_RE.match(value):
        raise InvalidStatementMonthError(
            f"Invalid statement month {statement_month!r}. Expected YYYY-MM with a real month."
        )
    return value


def find_existing_import_by_hash(db_path, file_hash: str):
    with connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, statement_month, source_path, imported_at FROM imports WHERE file_hash=? ORDER BY id ASC LIMIT 1",
            (file_hash,),
        )
        return cur.fetchone()


def ingest_broker_csv(db_path, csv_path: str | Path, statement_month: str, broker_name: str = "broker_csv") -> int:
    csv_path = Path(csv_path)
    normalized_statement_month = validate_statement_month(statement_month)
    rows, statement_totals = parse_csv(csv_path)
    file_hash = sha256_file(csv_path)

    existing = find_existing_import_by_hash(db_path, file_hash)
    if existing is not None:
        raise DuplicateImportError(
            "Duplicate broker CSV import blocked. "
            f"Existing import_id={existing['id']} statement_month={existing['statement_month']} "
            f"source_path={existing['source_path']} imported_at={existing['imported_at']}."
        )

    with connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO imports(source_path, broker_name, statement_month, file_hash) VALUES (?,?,?,?)",
            (str(csv_path), broker_name, normalized_statement_month, file_hash),
        )
        import_id = cur.lastrowid

        cur.executemany(
            """
            INSERT INTO broker_trades(import_id, trade_date, symbol, quantity, side, gross_pl, commissions_fees, net_pl, raw_row_json)
            VALUES (?,?,?,?,?,?,?,?,?)
            """,
            [
                (
                    import_id,
                    r["trade_date"],
                    r["symbol"],
                    r["quantity"],
                    r["side"],
                    r["gross_pl"],
                    r["commissions_fees"],
                    r["net_pl"],
                    json.dumps(r["raw"], sort_keys=True),
                )
                for r in rows
            ],
        )

        cur.execute(
            """
            INSERT INTO broker_statement_totals(import_id, statement_gross_pl, statement_fees, statement_net_pl, statement_beginning_balance, statement_ending_balance)
            VALUES (?,?,?,?,?,?)
            """,
            (
                import_id,
                statement_totals.get("statement_gross_pl"),
                statement_totals.get("statement_fees"),
                statement_totals.get("statement_net_pl"),
                statement_totals.get("statement_beginning_balance"),
                statement_totals.get("statement_ending_balance"),
            ),
        )

        conn.commit()
        return import_id
