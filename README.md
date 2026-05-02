# LedgerFlow Personal MVP

A reconciliation-first, local-first personal trading finance dashboard for a U.S. futures trader using §1256 contracts.

## What this repository is

This repository contains:

- a **personal-use MVP** for tracking broker P&L, expenses, assets, and estimated taxes
- a **GitHub-ready documentation set** covering product, architecture, testing, and ADRs
- **tax-oriented reference documents** for the intended use case: active futures trading, Trader Tax Status context, Schedule C expense tracking, and Puerto Rico Act 60 planning notes

This is deliberately **not** filing software and **not** legal or tax advice. It is a personal operating system for:

- reconciling broker-exported results
- measuring profit after trading costs and overhead
- planning tax set-asides conservatively
- preserving a clean audit trail for your own records and CPA handoff

## Product intent

LedgerFlow exists to solve one practical problem:

> Broker P&L is not the same thing as usable financial truth.

For a live futures trader, the real operating questions are:

- What did I actually make after direct trade costs?
- What did I spend on software, data, and equipment?
- What should I reserve for taxes?
- Can I trust the imported numbers?
- Is my monthly view consistent enough to support decisions?

The MVP answers those questions with a **reconciliation gate** at the center. If imported totals do not match statement totals, reporting is not trusted.

## Core principles

### 1. Reconciliation before insight
No dashboards are considered trustworthy unless computed totals reconcile to broker statement totals within tolerance.

### 2. Local-first by default
This personal version is designed to run on your own workstation. No cloud dependency is required.

### 3. Deterministic outputs
Same inputs + same settings = same outputs.

### 4. Guardrails against self-inflicted errors
The app explicitly avoids common mistakes such as double counting commissions as both direct trade costs and business expenses.

### 5. Tax-aware, not tax-automatic
This repository includes a conservative planning model, not a filing engine. Final reporting still belongs with a CPA or final tax software workflow.

## Intended user

This repository is tuned for a single user with the following profile:

- U.S. citizen
- actively trading futures or micro futures
- likely using §1256 contracts
- possibly qualifying for Trader Tax Status
- not electing §475 mark-to-market in the current design
- interested in future Puerto Rico Act 60 relocation planning
- wants a personal discipline tool before building commercial-grade software

## Current MVP capabilities

- CSV import of broker statement data
- storage of raw imports and normalized trade rows
- reconciliation of computed totals vs statement totals
- expenses ledger with business-use allocation
- asset register for workstation, monitors, and related purchases
- month dashboard
- YTD rollup
- quarterly planning schedule
- estimated tax and set-aside calculations using conservative effective rates
- export bundle generation as CSV files

## Non-goals

This repository does not currently attempt to do the following:

- e-file taxes
- provide legal or tax advice
- determine whether the user qualifies for Trader Tax Status
- automate IRS or Puerto Rico law updates
- support multi-user access
- support multiple brokers with heterogeneous schemas beyond the current sample shape
- serve as an authoritative accounting ledger for anyone except the local user who verifies results

## Repository layout

```text
.
├── README.md
├── pyproject.toml
├── app.py
├── src/ledgerflow/
│   ├── __init__.py
│   ├── db.py
│   ├── parse_broker_csv.py
│   ├── ingest.py
│   ├── reconcile.py
│   ├── metrics.py
│   ├── taxes.py
│   ├── exports.py
│   ├── settings.py
│   └── guardrails.py
└── docs/
    ├── 00_overview/
    ├── 01_product/
    ├── 02_architecture/
    ├── 03_interfaces/
    ├── 04_adrs/
    ├── 05_testing/
    ├── 06_tax/
    └── 07_runbooks/
```

## Running the app locally

### Requirements

- Python 3.11+
- Streamlit
- pandas

### Setup

```bash
uv sync
```

### Run

```bash
uv run streamlit run app.py
```

The app stores data in a local SQLite file under `data/ledgerflow.sqlite`.

## Data model summary

### imports
Tracks raw import provenance, statement month, file hash, and import timestamps.

### broker_trades
Stores normalized trade rows from the imported statement.

### broker_statement_totals
Stores statement-level totals used for reconciliation.

### expenses
Stores Schedule C-style business expense entries used for planning.

### assets
Stores workstation and equipment purchases, including business-use allocation and planning method.

### reconciliation
Stores reconciliation outcomes with explicit status and notes.

### settings
Stores persisted planning assumptions such as effective tax rate and set-aside buffer.

## Tax model summary

The app is intentionally conservative.

### Included

- direct trade costs from broker rows
- overhead expenses with business-use allocation
- simple estimated-tax planning based on effective rate assumptions
- quarterly and YTD planning views

### Excluded

- exact bracket computation
- full Form 6781 generation from raw executions
- formal Schedule C production suitable for filing without human review
- automated law changes

## Why this repo is structured heavily for documentation

This project is closer to a **risk and reconciliation system** than to a generic hobby app.
The documentation exists to preserve:

- invariants
- audit survivability
- implementation clarity
- separation between planning logic and filing logic

This is intentional. The docs are part of the product.

## Suggested workflow

### Monthly

1. Export broker statement CSV.
2. Import into LedgerFlow.
3. Check reconciliation status.
4. Enter expenses and asset purchases.
5. Review month dashboard and YTD rollup.
6. Export monthly bundle.

### Quarterly

1. Review estimated tax schedule.
2. Compare actual cash reserves vs set-aside target.
3. Recalibrate effective rate assumptions conservatively if needed.

## Where to start in the docs

- Product intent: `docs/01_product/`
- Architecture and invariants: `docs/02_architecture/`
- File interfaces: `docs/03_interfaces/`
- Durable design decisions: `docs/04_adrs/`
- Test strategy: `docs/05_testing/`
- Tax-specific notes: `docs/06_tax/`

## Important caution

Nothing in this repository should be used as a substitute for individualized tax or legal advice. This project is designed for disciplined personal planning and internal record-keeping.

## Next logical upgrades

- import de-duplication based on file hash
- richer exports
- settings snapshots embedded into exports
- multiple broker schemas
- YTD export bundle
- optional migration to a hosted UI after local validation
