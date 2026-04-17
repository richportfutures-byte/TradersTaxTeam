# Reconciliation Test Matrix

## Cases
1. Full anchors present, exact match => GREEN
2. Full anchors present, within tolerance => GREEN
3. Full anchors present, mismatch beyond tolerance => RED
4. Missing one or more anchors, computed values available => YELLOW
5. Missing required trade fields => import/parser failure

## Required assertions
- correct computed totals
- correct status classification
- clear notes field content
- export blocking behavior for RED
