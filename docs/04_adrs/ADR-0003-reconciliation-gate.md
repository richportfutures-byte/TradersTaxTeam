# ADR-0003: Reconciliation Gate Controls Trust

## Status
Accepted

## Context
Financial dashboards can create false certainty if they are not tied to statement-verified values.

## Decision
Use reconciliation status as the primary trust gate for reporting and exports.

## Consequences
### Positive
- prevents silent trust inflation
- makes integrity state visible

### Negative
- may frustrate users who want quick dashboards even when source data is incomplete
