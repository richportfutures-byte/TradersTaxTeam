from datetime import datetime
from pathlib import Path
import math

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


class BrokerCSVValidationError(ValueError):
    """Raised when a broker CSV cannot be safely normalized for import."""


def normalize(name: str) -> str:
    return "".join(ch.lower() for ch in str(name).strip() if ch.isalnum() or ch == "_")


def _clean_string(value) -> str:
    if pd.isna(value):
        raise BrokerCSVValidationError("Encountered a required blank field in broker CSV.")
    text = str(value).strip()
    if not text:
        raise BrokerCSVValidationError("Encountered an empty required text field in broker CSV.")
    return text


def _coerce_float(value, field_name: str) -> float:
    if pd.isna(value):
        raise BrokerCSVValidationError(f"Field '{field_name}' is blank and cannot be parsed as a number.")

    text = str(value).strip().replace(",", "").replace("$", "")
    negative = text.startswith("(") and text.endswith(")")
    if negative:
        text = text[1:-1].strip()

    try:
        out = float(text)
    except (TypeError, ValueError) as exc:
        raise BrokerCSVValidationError(f"Field '{field_name}' has a non-numeric value: {value!r}") from exc

    if negative:
        out = -out
    if not math.isfinite(out):
        raise BrokerCSVValidationError(f"Field '{field_name}' must be a finite number.")
    return out


def _coerce_optional_float(value):
    if pd.isna(value):
        return None
    text = str(value).strip()
    if not text:
        return None
    return _coerce_float(value, "optional_statement_field")


def _coerce_trade_date(value) -> str:
    text = _clean_string(value)
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    parsed = pd.to_datetime(text, errors="coerce")
    if pd.isna(parsed):
        raise BrokerCSVValidationError(f"TradeDate is not parseable: {value!r}")
    return parsed.strftime("%Y-%m-%d")


def _coerce_symbol(value) -> str:
    return _clean_string(value).upper()


def _coerce_side(value) -> str:
    side = _clean_string(value).upper()
    if side not in {"BUY", "SELL", "BOT", "SOLD", "LONG", "SHORT"}:
        raise BrokerCSVValidationError(
            f"Unsupported side value {value!r}. Expected one of BUY, SELL, BOT, SOLD, LONG, SHORT."
        )
    return side


def parse_csv(path: str | Path):
    df = pd.read_csv(path, dtype=object)
    raw_columns = list(df.columns)
    normalized_to_original = {normalize(c): c for c in raw_columns}

    missing = [k for k in REQUIRED_COLUMNS if k not in normalized_to_original]
    if missing:
        raise BrokerCSVValidationError(f"Missing required broker CSV columns: {missing}")

    rows = []
    for idx, row in df.iterrows():
        raw = {str(k): (None if pd.isna(v) else v) for k, v in row.to_dict().items()}
        try:
            normalized_row = {
                "trade_date": _coerce_trade_date(row[normalized_to_original["tradedate"]]),
                "symbol": _coerce_symbol(row[normalized_to_original["symbol"]]),
                "quantity": _coerce_float(row[normalized_to_original["quantity"]], "quantity"),
                "side": _coerce_side(row[normalized_to_original["side"]]),
                "gross_pl": _coerce_float(row[normalized_to_original["grosspl"]], "gross_pl"),
                "commissions_fees": _coerce_float(
                    row[normalized_to_original["commissions_fees"]],
                    "commissions_fees",
                ),
                "net_pl": _coerce_float(row[normalized_to_original["netpl"]], "net_pl"),
                "raw": raw,
            }
        except BrokerCSVValidationError as exc:
            raise BrokerCSVValidationError(f"Row {idx + 2}: {exc}") from exc
        rows.append(normalized_row)

    statement_totals = {}
    if len(df) > 0:
        first = df.iloc[0]
        for norm_name, target in OPTIONAL_STATEMENT_COLUMNS.items():
            if norm_name in normalized_to_original:
                statement_totals[target] = _coerce_optional_float(first[normalized_to_original[norm_name]])

    return rows, statement_totals
