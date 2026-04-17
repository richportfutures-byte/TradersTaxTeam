# Reconciliation Design

## Goal
Ensure reporting surfaces are trustworthy only when internally computed totals match broker statement anchors within tolerance.

## Inputs
- normalized trade rows
- statement-level totals when available
- configurable tolerance

## Computed values
- computed gross P&L
- computed fees
- computed net P&L

## Statement anchors
- statement gross P&L
- statement fees
- statement net P&L

## Status logic

### GREEN
- all required anchors available
- computed values match statement totals within tolerance

### YELLOW
- one or more statement anchors missing
- enough data exists for provisional planning
- outputs must be labeled provisional

### RED
- anchors present and mismatch exceeds tolerance
- import cannot be trusted for final reporting/export

## Behavior requirements
- reconciliation is triggered immediately after import
- reconciliation notes should explain missing anchors or deltas
- RED must visibly block trusted export surfaces
- user should be able to inspect raw deltas

## Philosophy
The system should fail closed on trust. A pretty dashboard is not a substitute for matching totals.
