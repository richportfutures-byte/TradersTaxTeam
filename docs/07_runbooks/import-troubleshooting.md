# Import Troubleshooting

## Problem: CSV fails to parse
Check:
- required columns exist
- numeric columns use parseable formatting
- date column is valid

## Problem: reconciliation is RED
Check:
- statement-level anchors are present and correctly mapped
- broker CSV includes all rows for the month
- fees are not double counted
- imported statement month is correct

## Problem: reconciliation is YELLOW
Check whether the broker export omitted statement-level totals. Planning views may still be usable, but not as fully trusted reporting.
