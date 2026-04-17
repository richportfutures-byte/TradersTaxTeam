# ADR-0004: Local MVP Uses SQLite, Future Hosted Version May Use Postgres + Object Store

## Status
Accepted

## Context
The personal MVP should run locally with minimal setup. A future hosted version may need stronger storage primitives.

## Decision
Use SQLite now. Preserve future migration path to Postgres for structured data and object storage for source files/exports.

## Consequences
### Positive
- easy local setup
- no infrastructure dependency

### Negative
- not intended for concurrent multi-user workloads
