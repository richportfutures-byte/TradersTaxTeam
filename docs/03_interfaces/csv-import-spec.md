# CSV Import Specification

## Purpose
Define the expected minimal broker CSV interface for MVP.

## Required row-level fields
- TradeDate
- Symbol
- Quantity
- Side
- GrossPL
- Commissions_Fees
- NetPL

## Optional statement-level fields
- StatementGrossPL
- StatementFees
- StatementNetPL
- BeginningBalance
- EndingBalance

## Semantics
- GrossPL = trading result before fees
- Commissions_Fees = execution-related costs already embedded in broker net performance
- NetPL = GrossPL - Commissions_Fees

## Parser behavior
- normalize column names
- trim whitespace
- coerce numeric columns safely
- reject missing required columns
- allow optional statement totals
- attach raw row JSON for auditability

## Known limitation
This spec assumes a reasonably clean CSV export. Future versions may need broker-specific adapters.
