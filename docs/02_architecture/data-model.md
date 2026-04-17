# Data Model

## Purpose
Define the persistent entities used in LedgerFlow Personal MVP.

## Entities

### imports
Tracks a broker CSV import event.
Fields:
- id
- source_path
- broker_name
- statement_month
- file_hash
- imported_at

### broker_trades
Stores normalized trade rows.
Representative fields:
- import_id
- trade_date
- symbol
- quantity
- side
- gross_pl
- commissions_fees
- net_pl
- raw_row_json

### broker_statement_totals
Stores statement-level totals imported or inferred from the statement export.
Representative fields:
- import_id
- statement_gross_pl
- statement_fees
- statement_net_pl
- statement_beginning_balance
- statement_ending_balance

### expenses
Stores manually entered business-use operating expenses.
Representative fields:
- date
- vendor
- category
- amount
- business_use_pct
- memo

### assets
Stores larger equipment purchases.
Representative fields:
- description
- cost
- placed_in_service_date
- business_use_pct
- method

### reconciliation
Stores computed reconciliation results.
Representative fields:
- import_id
- status
- computed_gross_pl
- computed_fees
- computed_net_pl
- delta_gross_pl
- delta_fees
- delta_net_pl
- notes
- reconciled_at

### settings
Stores persisted user planning settings.
Representative fields:
- key
- value
- updated_at

## Modeling rules
- imported raw facts are append-only at the import layer
- normalized rows retain provenance back to import_id
- reconciliation results are explicit, not implicit
- expense data is separate from broker-derived trade costs
- asset treatment is planning metadata, not filing automation
