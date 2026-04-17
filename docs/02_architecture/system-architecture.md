# System Architecture

## Style
Modular monolith, local-first.

## Core layers

### 1. Ingestion
Responsible for parsing broker CSV input, validating required fields, storing raw provenance, and producing normalized trade rows and statement totals.

### 2. Reconciliation
Responsible for computing totals from normalized rows and comparing them against broker statement anchors. Produces GREEN/YELLOW/RED status.

### 3. Metrics
Responsible for period summaries, YTD summaries, and quarterly rollups after direct costs and overhead.

### 4. Tax planning
Responsible for applying simple planning assumptions such as effective tax rate and set-aside buffer.

### 5. Exports
Responsible for generating CSV bundles with visible trust context.

### 6. UI
Responsible for import workflow, dashboards, expense entry, asset entry, and exports.

## Runtime choices
- Python application
- Streamlit UI
- SQLite for local persistence
- CSV as first import/export format

## Trust boundary
Everything downstream of import depends on reconciliation state. UI must not hide this.
