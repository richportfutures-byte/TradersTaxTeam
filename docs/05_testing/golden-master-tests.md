# Golden-Master Tests

## Purpose
Protect against parser regressions and schema drift.

## Strategy
- maintain one or more representative broker CSV fixtures
- assert parsed row counts, summed gross P&L, summed fees, summed net P&L
- assert statement-level anchors when present
- assert reconciliation status against known fixture expectations

## Why this matters
If import semantics drift, all downstream reporting becomes suspect.
