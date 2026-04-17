from dataclasses import dataclass

from .db import connect


@dataclass
class PeriodSummary:
    gross_pl: float
    direct_fees: float
    net_pl: float
    overhead_expenses: float
    profit_after_costs: float


def _sum_or_zero(value):
    return float(value or 0.0)


def get_period_summary(db_path, statement_month: str) -> PeriodSummary:
    with connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                COALESCE(SUM(t.gross_pl),0),
                COALESCE(SUM(t.commissions_fees),0),
                COALESCE(SUM(t.net_pl),0)
            FROM broker_trades t
            JOIN imports i ON i.id = t.import_id
            WHERE i.statement_month = ?
            """,
            (statement_month,),
        )
        gross, fees, net = map(_sum_or_zero, cur.fetchone())

        cur.execute(
            "SELECT COALESCE(SUM(amount * business_use_pct),0) FROM expenses WHERE substr(date,1,7)=?",
            (statement_month,),
        )
        overhead = _sum_or_zero(cur.fetchone()[0])

    return PeriodSummary(
        gross_pl=gross,
        direct_fees=fees,
        net_pl=net,
        overhead_expenses=overhead,
        profit_after_costs=net - overhead,
    )


def get_ytd_summary(db_path, year: int) -> PeriodSummary:
    prefix = f"{year:04d}-"
    with connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                COALESCE(SUM(t.gross_pl),0),
                COALESCE(SUM(t.commissions_fees),0),
                COALESCE(SUM(t.net_pl),0)
            FROM broker_trades t
            JOIN imports i ON i.id = t.import_id
            WHERE i.statement_month LIKE ?
            """,
            (f"{prefix}%",),
        )
        gross, fees, net = map(_sum_or_zero, cur.fetchone())

        cur.execute(
            "SELECT COALESCE(SUM(amount * business_use_pct),0) FROM expenses WHERE substr(date,1,4)=?",
            (f"{year:04d}",),
        )
        overhead = _sum_or_zero(cur.fetchone()[0])

    return PeriodSummary(
        gross_pl=gross,
        direct_fees=fees,
        net_pl=net,
        overhead_expenses=overhead,
        profit_after_costs=net - overhead,
    )


def quarterly_profit_after_costs(db_path, year: int) -> dict[str, float]:
    out = {"Q1": 0.0, "Q2": 0.0, "Q3": 0.0, "Q4": 0.0}
    for month in range(1, 13):
        statement_month = f"{year:04d}-{month:02d}"
        p = get_period_summary(db_path, statement_month)
        q = (month - 1) // 3 + 1
        out[f"Q{q}"] += p.profit_after_costs
    return out
