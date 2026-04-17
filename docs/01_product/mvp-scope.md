# MVP Scope

This document defines the minimum viable product for LedgerFlow Personal MVP.

## In scope

### Broker data
- import broker CSV files manually
- parse row-level trade and fee data
- store raw import provenance and normalized records
- store statement-level totals when present

### Reconciliation
- compute internal totals from imported rows
- compare internal totals vs statement totals
- assign reconciliation status GREEN/YELLOW/RED
- block trusted exports when reconciliation is RED

### Operating expense tracking
- manual entry of business-use expenses
- allocation by business-use percentage
- category-based organization
- separation from direct trade costs

### Asset tracking
- manual entry of larger purchases such as workstation, monitors, desk, UPS, networking equipment
- business-use allocation
- simple method tagging for planning only (Section 179 vs depreciate)

### Dashboards
- monthly summary
- YTD summary
- quarterly planning rollup
- visible tax planning estimates and set-aside targets

### Exports
- monthly summary CSV
- expenses CSV
- assets CSV
- reconciliation report CSV

## Out of scope
- tax return generation
- exact multi-jurisdiction tax logic
- document OCR
- receipt ingestion pipeline
- entity consolidation
- collaboration workflow
- permissions
- cloud hosting requirements

## Success condition
The MVP succeeds if the user can do a disciplined monthly close and answer:
- did my imported broker totals reconcile?
- what was my real profit after direct costs and overhead?
- what should I set aside for taxes?
- what records can I hand to myself or a CPA later?
