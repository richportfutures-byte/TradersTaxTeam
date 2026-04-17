# ADR-0002: Planning Rules Should Be Versioned and Curated

## Status
Accepted

## Context
Tax planning assumptions may change over time, and ad hoc changes hidden in logic are dangerous.

## Decision
Preserve architecture room for explicit rulepack/versioning even if MVP uses a simple implicit rulepack.

## Consequences
### Positive
- future tax logic changes become traceable
- exports can preserve policy context

### Negative
- adds conceptual overhead before full implementation
