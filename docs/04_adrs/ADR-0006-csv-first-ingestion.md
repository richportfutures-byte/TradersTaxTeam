# ADR-0006: CSV-First Ingestion for MVP

## Status
Accepted

## Context
Broker integrations are highly variable and often not worth the integration burden for a personal MVP.

## Decision
Support manual CSV import first, with broker-specific normalization inside the parser rather than live API integration.

## Consequences
### Positive
- faster MVP delivery
- simpler trust model

### Negative
- manual import workflow remains necessary
