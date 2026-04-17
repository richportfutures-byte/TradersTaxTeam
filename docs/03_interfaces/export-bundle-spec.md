# Export Bundle Specification

## Purpose
Define the monthly export bundle produced by LedgerFlow MVP.

## Files
- monthly_summary.csv
- expenses.csv
- assets.csv
- reconciliation.csv

## Required fields: monthly_summary.csv
- statement_month
- gross_pl
- direct_fees
- net_pl
- overhead_expenses
- profit_after_costs
- effective_tax_rate
- set_aside_buffer
- est_tax
- est_after_tax_profit
- set_aside_target

## Required fields: reconciliation.csv
- import_id
- status
- computed_gross_pl
- computed_fees
- computed_net_pl
- delta_gross_pl
- delta_fees
- delta_net_pl
- notes

## Trust requirement
If any import for the period is RED, export generation for trusted reporting should be blocked or explicitly marked untrusted.

## Future extension
- rulepack/version metadata
- source file hash metadata
- YTD summary bundle
