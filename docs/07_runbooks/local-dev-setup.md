# Local Development Setup

## Requirements
- Python 3.11+
- virtualenv/venv

## Steps
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
streamlit run app.py
```

## Storage
The app creates a local SQLite DB file under `data/ledgerflow.sqlite`.
