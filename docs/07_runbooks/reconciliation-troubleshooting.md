# Reconciliation Troubleshooting

## RED state meaning
Computed totals do not match broker statement anchors within tolerance. Reporting/export should be treated as untrusted until resolved.

## Resolution sequence
1. inspect statement month
2. inspect imported row count
3. inspect gross/fees/net computed totals
4. compare against statement anchors
5. inspect notes field for missing anchors or mismatches

## Discipline rule
Do not trust a pretty dashboard over a failed reconciliation.
