import sqlite3
from pathlib import Path

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS imports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_path TEXT NOT NULL,
    broker_name TEXT NOT NULL DEFAULT 'broker_csv',
    statement_month TEXT NOT NULL,
    file_hash TEXT NOT NULL,
    imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS broker_trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    import_id INTEGER NOT NULL REFERENCES imports(id) ON DELETE CASCADE,
    trade_date TEXT NOT NULL,
    symbol TEXT NOT NULL,
    quantity REAL NOT NULL,
    side TEXT NOT NULL,
    gross_pl REAL NOT NULL,
    commissions_fees REAL NOT NULL,
    net_pl REAL NOT NULL,
    raw_row_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS broker_statement_totals (
    import_id INTEGER PRIMARY KEY REFERENCES imports(id) ON DELETE CASCADE,
    statement_gross_pl REAL,
    statement_fees REAL,
    statement_net_pl REAL,
    statement_beginning_balance REAL,
    statement_ending_balance REAL
);

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    vendor TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    business_use_pct REAL NOT NULL,
    memo TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    cost REAL NOT NULL,
    placed_in_service_date TEXT NOT NULL,
    business_use_pct REAL NOT NULL,
    method TEXT NOT NULL CHECK(method IN ('179', 'depreciate'))
);

CREATE TABLE IF NOT EXISTS reconciliation (
    import_id INTEGER PRIMARY KEY REFERENCES imports(id) ON DELETE CASCADE,
    status TEXT NOT NULL CHECK(status IN ('GREEN', 'YELLOW', 'RED')),
    computed_gross_pl REAL NOT NULL,
    computed_fees REAL NOT NULL,
    computed_net_pl REAL NOT NULL,
    delta_gross_pl REAL,
    delta_fees REAL,
    delta_net_pl REAL,
    notes TEXT NOT NULL DEFAULT '',
    reconciled_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_imports_statement_month ON imports(statement_month);
CREATE INDEX IF NOT EXISTS idx_imports_file_hash ON imports(file_hash);
CREATE INDEX IF NOT EXISTS idx_broker_trades_import_id ON broker_trades(import_id);
CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date);
CREATE INDEX IF NOT EXISTS idx_assets_placed_in_service_date ON assets(placed_in_service_date);
"""


def connect(db_path: str | Path):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection):
    conn.executescript(SCHEMA_SQL)
    conn.commit()
