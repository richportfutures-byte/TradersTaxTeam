# Local Development Setup

## Requirements
- Python 3.11+
- uv

## Steps
```bash
uv sync
uv run streamlit run app.py
```

## Storage
The app creates a local SQLite DB file under `data/ledgerflow.sqlite`.
