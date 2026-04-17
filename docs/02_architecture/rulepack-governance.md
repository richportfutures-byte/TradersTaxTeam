# Rulepack Governance

## Purpose
LedgerFlow MVP uses simple planning logic now, but the architecture should preserve room for explicit, versioned rulepacks.

## Why rulepacks exist
Tax planning logic changes over time, and future versions may need explicit policy bundles rather than hard-coded assumptions.

## MVP posture
- one implicit rulepack
- conservative estimated-tax logic
- configurable effective tax rate and set-aside buffer

## Future-ready governance requirements
- every rulepack should have an identifier and version
- exports should record which rulepack/settings were active
- rulepacks should separate planning policy from raw facts
- migration between rulepacks must not silently mutate historical raw data

## Anti-patterns
- hidden assumptions scattered across UI and calculation code
- changing tax logic without version traceability
- using AI-generated tax advice as an implicit rulepack
