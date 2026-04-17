# Test Strategy

## Priority order
1. parser correctness
2. reconciliation correctness
3. guardrails around expense categorization and trust blocking
4. export content correctness
5. UI smoke tests

## Minimum test set
- fixture import succeeds
- bad schema import fails loudly
- GREEN/YELLOW/RED status logic behaves deterministically
- expenses do not alter broker direct fee totals
- monthly export bundle contains expected columns
