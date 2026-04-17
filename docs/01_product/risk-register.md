# Risk Register

## R1: Broker schema drift
**Risk**: CSV columns or semantics change.
**Impact**: bad parse, wrong totals, false dashboard values.
**Mitigation**: explicit import spec, parser validation, sample golden-master tests.

## R2: Double counting commissions
**Risk**: user enters execution costs as expenses after broker net already includes them.
**Impact**: profit understated, tax planning distorted.
**Mitigation**: hard UI guardrails, docs, category validation.

## R3: Partial statement totals
**Risk**: statement lacks one or more anchors needed for full reconciliation.
**Impact**: false certainty.
**Mitigation**: YELLOW status, visible uncertainty language.

## R4: Over-trust in estimated tax outputs
**Risk**: user treats planning numbers as final tax truth.
**Impact**: underpayment or bad decisions.
**Mitigation**: explicit disclaimers, simple settings, no filing posture.

## R5: Scope creep
**Risk**: project tries to become full bookkeeping/tax software.
**Impact**: complexity explosion, loss of trust.
**Mitigation**: strict non-goals, ADR governance.
