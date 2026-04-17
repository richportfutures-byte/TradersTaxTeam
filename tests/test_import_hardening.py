import tempfile
import unittest
from pathlib import Path

from ledgerflow.db import connect, init_db
from ledgerflow.ingest import (
    DuplicateImportError,
    InvalidStatementMonthError,
    ingest_broker_csv,
    validate_statement_month,
)
from ledgerflow.parse_broker_csv import BrokerCSVValidationError, parse_csv


VALID_CSV = """TradeDate,Symbol,Quantity,Side,GrossPL,Commissions_Fees,NetPL,StatementGrossPL,StatementFees,StatementNetPL
2025-01-02,MNQ,1,buy,100.00,2.50,97.50,100.00,2.50,97.50
2025-01-03,MNQ,1,sell,-50.00,2.50,-52.50,100.00,2.50,97.50
"""

INVALID_SIDE_CSV = """TradeDate,Symbol,Quantity,Side,GrossPL,Commissions_Fees,NetPL
2025-01-02,MNQ,1,hold,100.00,2.50,97.50
"""


class ImportHardeningTests(unittest.TestCase):
    def test_validate_statement_month_accepts_real_yyyy_mm(self):
        self.assertEqual(validate_statement_month("2025-01"), "2025-01")

    def test_validate_statement_month_rejects_bad_format(self):
        with self.assertRaises(InvalidStatementMonthError):
            validate_statement_month("2025-13")

        with self.assertRaises(InvalidStatementMonthError):
            validate_statement_month("2025-1")

    def test_parse_csv_normalizes_trade_date_and_side(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "broker.csv"
            csv_path.write_text(VALID_CSV, encoding="utf-8")

            rows, totals = parse_csv(csv_path)

            self.assertEqual(rows[0]["trade_date"], "2025-01-02")
            self.assertEqual(rows[0]["symbol"], "MNQ")
            self.assertEqual(rows[0]["side"], "BUY")
            self.assertEqual(totals["statement_net_pl"], 97.50)

    def test_parse_csv_rejects_unsupported_side(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "broker.csv"
            csv_path.write_text(INVALID_SIDE_CSV, encoding="utf-8")

            with self.assertRaises(BrokerCSVValidationError):
                parse_csv(csv_path)

    def test_duplicate_import_is_blocked_by_file_hash(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "ledgerflow.sqlite"
            csv_path = Path(tmpdir) / "broker.csv"
            csv_path.write_text(VALID_CSV, encoding="utf-8")

            conn = connect(db_path)
            init_db(conn)
            conn.close()

            first_import_id = ingest_broker_csv(db_path, csv_path, "2025-01")
            self.assertEqual(first_import_id, 1)

            with self.assertRaises(DuplicateImportError):
                ingest_broker_csv(db_path, csv_path, "2025-01")


if __name__ == "__main__":
    unittest.main()
