# ADR-0005: Import Provenance and Audit Context Should Be Append-Only

## Status
Accepted

## Context
This system exists partly to preserve durable records and trust state.

## Decision
Treat import provenance and core audit context as append-only records.

## Consequences
### Positive
- better traceability
- easier reconstruction of historical workflow

### Negative
- requires more care when correcting bad imports
