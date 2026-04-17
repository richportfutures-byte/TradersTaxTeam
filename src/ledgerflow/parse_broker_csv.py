from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {
    "tradedate": "trade_date",
    "symbol": "symbol",
    "quantity": "quantity",
    "side": "side",
    "grosspl": "gross_pl",
    "commissions_fees": "commissions_fees",
    "netpl": "net_pl",
}

OPTIONAL_STATEMENT_COLUMNS = {
    "statementgrosspl": "statement_gross_pl",
    "statementfees": "statement_fees",
    "statementnetpl": "statement_net_pl",
    "beginningbalance": "statement_beginning_balance",
    "endingbalance": "statement_ending_balance",
}


def normalize(name: str) -> str:
    return "".join(ch.lower() for ch in str(name).strip() if ch.isalnum() or ch == "_")


def parse_csv(path: str | Path):
    df = pd.read_csv(path)
    raw_columns = list(df.columns)
    colmap = {c: normalize(c) for c in raw_columns}
    normalized_to_original = {normalize(c): c for c in raw_columns}

    missing = [k for k in REQUIRED_COLUMNS if k not in normalized_to_original]
    if missing:
        raise ValueError(f"Missing required broker CSV columns: {missing}")

    rows = []
    for _, row in df.iterrows():
        raw = {str(k): (None if pd.isna(v) else v) for k, v in row.to_dict().items()}
        rows.append(
            {
                "trade_date": str(row[normalized_to_original["tradedate"]]),
                "symbol": str(row[normalized_to_original["symbol"]]),
                "quantity": float(row[normalized_to_original["quantity"]]),
                "side": str(row[normalized_to_original["side"]]),
                "gross_pl": float(row[normalized_to_original["grosspl"]]),
                "commissions_fees": float(row[normalized_to_original["commissions_fees"]]),
                "net_pl": float(row[normalized_to_original["netpl"]]),
                "raw": raw,
            }
        )

    statement_totals = {}
    if len(df) > 0:
        first = df.iloc[0]
        for norm_name, target in OPTIONAL_STATEMENT_COLUMNS.items():
            if norm_name in normalized_to_original:
                value = first[normalized_to_original[norm_name]]
                statement_totals[target] = None if pd.isna(value) else float(value)

    return rows, statement_totals
