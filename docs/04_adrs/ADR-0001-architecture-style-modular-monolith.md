# ADR-0001: Architecture Style = Modular Monolith

## Status
Accepted

## Context
The project is personal-use MVP software with tightly coupled workflows across import, reconciliation, metrics, taxes, and export. Premature service decomposition would add complexity without operational value.

## Decision
Use a modular monolith implemented in a single Python codebase with clear module boundaries.

## Consequences
### Positive
- simple local deployment
- easy debugging
- low operational burden

### Negative
- future scaling boundaries must be refactored later if needed
