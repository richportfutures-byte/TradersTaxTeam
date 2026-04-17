# Product Requirements Document (PRD)

## Product name
LedgerFlow Personal MVP

## Problem statement
Broker P&L alone does not provide a trustworthy view of operating profitability, business overhead, or tax planning readiness for an active futures trader. A trader needs a disciplined, reconciliation-first personal system that transforms broker exports into usable monthly and YTD financial visibility without pretending to be tax filing software.

## Target user
Single-user active futures trader in the U.S. with tax-awareness needs, possible Trader Tax Status context, and desire for future Puerto Rico planning.

## Primary jobs to be done
1. Import broker-exported CSV data.
2. Verify whether internal totals reconcile to statement totals.
3. Track separate business operating expenses.
4. Track equipment/assets with business-use allocation.
5. View month/YTD profitability after costs.
6. View estimated tax and reserve targets.
7. Export structured monthly records.

## Product principles
- reconciliation before trust
- explicit uncertainty
- local-first operation
- conservative tax planning
- deterministic outputs
- no false automation theater

## User stories
- As a trader, I want to upload a broker CSV and immediately see whether I can trust the computed totals.
- As a trader, I want direct trade costs kept separate from overhead expenses.
- As a trader, I want monthly and YTD views after overhead so I can make real spending decisions.
- As a trader, I want simple estimated tax reserve targets so I stop confusing gross profitability with usable cash.
- As a trader, I want export bundles I can archive and later hand to a CPA or use for my own year-end review.

## Functional requirements
1. Accept broker CSV upload.
2. Store raw import provenance and normalized rows.
3. Store statement totals if present.
4. Compute internal totals and reconcile against statement totals.
5. Assign GREEN/YELLOW/RED reconciliation state.
6. Maintain separate expenses table.
7. Maintain assets table.
8. Compute monthly and YTD summaries.
9. Compute estimated tax and set-aside targets from configurable assumptions.
10. Export monthly bundle.

## Non-functional requirements
- must run locally
- must use deterministic calculations
- must preserve auditability
- must make red-state reporting visibly untrusted
- must be understandable without accounting jargon overload

## Risks
- broker CSV schema drift
- false confidence from partial statement data
- accidental double counting of direct trade costs as expenses
- user over-trust in planning estimates

## MVP exit criteria
- successful import of representative broker CSV
- visible reconciliation state
- visible monthly + YTD dashboard
- export bundle generated
- no silent mismatch between imported statement totals and computed values
