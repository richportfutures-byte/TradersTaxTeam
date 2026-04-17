from pathlib import Path
import pandas as pd

from .db import connect
from .metrics import get_period_summary
from .taxes import estimate_taxes


def export_monthly_bundle(db_path, statement_month: str, export_dir: str | Path, effective_tax_rate: float, set_aside_buffer: float):
    export_dir = Path(export_dir)
    export_dir.mkdir(parents=True, exist_ok=True)

    summary = get_period_summary(db_path, statement_month)
    tax = estimate_taxes(summary.profit_after_costs, effective_tax_rate, set_aside_buffer)

    summary_df = pd.DataFrame([
        {
            "statement_month": statement_month,
            "gross_pl": summary.gross_pl,
            "direct_fees": summary.direct_fees,
            "net_pl": summary.net_pl,
            "overhead_expenses": summary.overhead_expenses,
            "profit_after_costs": summary.profit_after_costs,
            "effective_tax_rate": effective_tax_rate,
            "set_aside_buffer": set_aside_buffer,
            "est_tax": tax.est_tax,
            "est_after_tax_profit": tax.est_after_tax_profit,
            "set_aside_target": tax.set_aside_target,
        }
    ])

    with connect(db_path) as conn:
        expenses = pd.read_sql_query(
            "SELECT date, vendor, category, amount, business_use_pct, memo, amount * business_use_pct AS allocated_amount "
            "FROM expenses WHERE substr(date,1,7)=? ORDER BY date ASC",
            conn,
            params=(statement_month,),
        )
        assets = pd.read_sql_query(
            "SELECT description, cost, placed_in_service_date, business_use_pct, method, cost * business_use_pct AS allocated_basis "
            "FROM assets WHERE substr(placed_in_service_date,1,7)=? ORDER BY placed_in_service_date ASC",
            conn,
            params=(statement_month,),
        )
        reconciliation = pd.read_sql_query(
            "SELECT r.* FROM reconciliation r JOIN imports i ON i.id = r.import_id WHERE i.statement_month=? ORDER BY r.import_id ASC",
            conn,
            params=(statement_month,),
        )

    base = export_dir / f"ledgerflow_{statement_month}"
    summary_df.to_csv(base.with_suffix(".monthly_summary.csv"), index=False)
    expenses.to_csv(base.with_suffix(".expenses.csv"), index=False)
    assets.to_csv(base.with_suffix(".assets.csv"), index=False)
    reconciliation.to_csv(base.with_suffix(".reconciliation.csv"), index=False)
    return base
