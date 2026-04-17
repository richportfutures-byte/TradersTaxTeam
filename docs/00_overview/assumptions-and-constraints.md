# Assumptions and Constraints

This document defines the operational assumptions and hard constraints for LedgerFlow Personal MVP.

## Assumptions

### User profile
- single-user personal deployment
- U.S. taxpayer
- active trader of futures and micro futures
- likely using Section 1256 contracts
- may be seeking or holding Trader Tax Status
- not currently electing Section 475 mark-to-market in MVP scope
- interested in future Puerto Rico Act 60 relocation planning

### Operating mode
- local-first deployment
- workstation or laptop use
- user imports broker CSVs manually
- user reviews reconciliation outcomes before trusting output
- user maintains supporting receipts and source documents outside the app

### Data assumptions
- broker exports contain enough row-level and/or statement-level data to compute period P&L and fee totals
- dates are present and parseable
- imported CSVs are not authoritative until reconciliation passes
- brokerage data may need normalization before reporting

### Accounting/tax assumptions
- the app is for planning and record organization, not for direct tax filing
- business expense treatment is user-entered and may require CPA validation
- direct trade costs and Schedule C-style operating expenses must remain separate
- estimated tax logic is approximate and policy-driven, not authoritative law automation

## Hard constraints

### Product constraints
- no tax filing engine in MVP
- no legal/tax advice engine
- no brokerage API dependency in MVP
- no multi-user collaboration in MVP
- no cloud dependency required for core operation

### Trust constraints
- dashboard values are not trustworthy unless reconciled to broker statement totals
- exports must indicate whether reconciliation was GREEN/YELLOW/RED
- any mismatch should fail closed for "trusted" reporting surfaces

### Modeling constraints
- no silent imputation of missing statement totals
- no hidden tax assumptions beyond documented settings or rulepacks
- no mixing of direct trading costs with overhead expenses
- no automated determination of Trader Tax Status qualification

### UX constraints
- the app must make uncertainty visible
- the app must not present estimates as certified tax truth
- the app should support a disciplined monthly workflow, not maximize feature breadth

## Design implication
LedgerFlow is not a general accounting platform. It is a constrained personal operating tool for trading finance visibility under uncertainty.
