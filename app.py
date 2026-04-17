from pathlib import Path
import pandas as pd
import streamlit as st

from ledgerflow.db import connect, init_db
from ledgerflow.ingest import ingest_broker_csv
from ledgerflow.reconcile import reconcile_import
from ledgerflow.metrics import get_period_summary, get_ytd_summary, quarterly_profit_after_costs
from ledgerflow.taxes import estimate_taxes, quarterly_estimates
from ledgerflow.exports import export_monthly_bundle
from ledgerflow.settings import get_setting, set_setting
from ledgerflow.guardrails import validate_expense_category

DB_PATH = Path("data/ledgerflow.sqlite")
EXPORT_DIR = Path("data/exports")


def load_df(conn, query, params=()):
    return pd.read_sql_query(query, conn, params=params)


def reconciliation_banner(status: str | None, notes: str = ""):
    if status is None:
        st.info("Reconciliation: not evaluated for this import.")
        return
    if status == "GREEN":
        st.success("Reconciliation GREEN — totals match within tolerance.")
    elif status == "YELLOW":
        st.warning("Reconciliation YELLOW — computed totals available but missing statement anchors.")
    else:
        st.error("Reconciliation RED — mismatch detected. Reporting and exports are untrusted until resolved.")
    if notes and notes.strip():
        with st.expander("Reconciliation notes"):
            st.code(notes)


def export_readiness(conn, statement_month: str):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT COUNT(*)
        FROM reconciliation r
        JOIN imports i ON i.id = r.import_id
        WHERE i.statement_month = ? AND r.status = 'RED'
        """,
        (statement_month,),
    )
    red_count = cur.fetchone()[0]
    if red_count > 0:
        st.error(f"Export readiness: BLOCKED — {red_count} import(s) in {statement_month} are RED.")
        return False
    st.success("Export readiness: OK — no RED reconciliations found for this month.")
    return True


st.set_page_config(page_title="LedgerFlow (Personal MVP)", layout="wide")
st.title("LedgerFlow — Personal MVP v0.2")

conn = connect(DB_PATH)
init_db(conn)

st.sidebar.header("Controls")
imports = load_df(conn, "SELECT * FROM imports ORDER BY imported_at DESC")

if imports.empty:
    st.sidebar.info("No imports yet. Use the Import tab to upload a CSV.")
    selected_import_id = None
    available_months = []
else:
    selected_import_id = int(st.sidebar.selectbox("Select import_id", imports["id"].tolist()))
    available_months = sorted(imports["statement_month"].dropna().unique().tolist(), reverse=True)

st.sidebar.divider()
st.sidebar.subheader("Reporting period")
manual_override = st.sidebar.toggle("Manual month override", value=False)

if manual_override or not available_months:
    selected_month = st.sidebar.text_input("Statement month (YYYY-MM)", value=available_months[0] if available_months else "2025-12")
else:
    selected_month = st.sidebar.selectbox("Statement month", options=available_months, index=0)

st.sidebar.divider()
st.sidebar.subheader("Planning settings (persisted)")
default_rate = float(get_setting(DB_PATH, "effective_tax_rate", "0.40"))
default_buffer = float(get_setting(DB_PATH, "set_aside_buffer", "0.05"))

effective_tax_rate = st.sidebar.slider("Effective tax rate", 0.0, 0.70, default_rate, 0.01)
set_aside_buffer = st.sidebar.slider("Set-aside buffer", 0.0, 0.25, default_buffer, 0.01)

if st.sidebar.button("Save planning settings"):
    set_setting(DB_PATH, "effective_tax_rate", str(effective_tax_rate))
    set_setting(DB_PATH, "set_aside_buffer", str(set_aside_buffer))
    st.sidebar.success("Saved.")

status = None
notes = ""
totals = pd.DataFrame()
trades = pd.DataFrame()
if selected_import_id is not None:
    rec = load_df(conn, "SELECT * FROM reconciliation WHERE import_id=?", (selected_import_id,))
    if not rec.empty:
        status = rec.loc[0, "status"]
        notes = rec.loc[0, "notes"] or ""
    totals = load_df(conn, "SELECT * FROM broker_statement_totals WHERE import_id=?", (selected_import_id,))
    trades = load_df(conn, "SELECT * FROM broker_trades WHERE import_id=? ORDER BY trade_date", (selected_import_id,))

reconciliation_banner(status, notes)

tab_import, tab_dash, tab_exp, tab_assets, tab_exports = st.tabs(
    ["1) Import & Reconcile", "2) Dashboard", "3) Expenses", "4) Assets", "5) Exports"]
)

with tab_import:
    st.subheader("Import broker CSV and reconcile immediately")
    c1, c2 = st.columns([2, 1])
    statement_month = c1.text_input("Statement month (YYYY-MM)", value=selected_month)
    tol = c2.number_input("Reconciliation tolerance", min_value=0.0, value=0.01, step=0.01)
    uploaded = st.file_uploader("Upload broker CSV", type=["csv"])

    if uploaded is not None:
        tmp_path = Path("data/imports") / uploaded.name
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path.write_bytes(uploaded.getvalue())
        st.caption(f"Staged file: {tmp_path}")
        if st.button("Import & Reconcile now"):
            import_id = ingest_broker_csv(DB_PATH, tmp_path, statement_month)
            reconcile_import(DB_PATH, import_id, tolerance=float(tol))
            st.success(f"Imported import_id={import_id}. Refresh the sidebar selector to view it.")

    st.subheader("Recent imports")
    st.dataframe(imports, use_container_width=True)

with tab_dash:
    st.subheader(f"Month dashboard — {selected_month}")
    summary = get_period_summary(DB_PATH, selected_month)
    tax = estimate_taxes(summary.profit_after_costs, effective_tax_rate, set_aside_buffer)

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Gross P&L", f"{summary.gross_pl:,.2f}")
    k2.metric("Direct fees", f"{summary.direct_fees:,.2f}")
    k3.metric("Net P&L", f"{summary.net_pl:,.2f}")
    k4.metric("Overhead (allocated)", f"{summary.overhead_expenses:,.2f}")
    k5.metric("Profit after costs", f"{summary.profit_after_costs:,.2f}")

    k6, k7, k8 = st.columns(3)
    k6.metric("Est. tax (month)", f"{tax.est_tax:,.2f}")
    k7.metric("Set-aside target (month)", f"{tax.set_aside_target:,.2f}")
    k8.metric("After-tax profit (month)", f"{tax.est_after_tax_profit:,.2f}")

    st.divider()
    if not trades.empty:
        st.subheader("Daily net P&L (trend)")
        t = trades.copy()
        t["trade_date"] = pd.to_datetime(t["trade_date"])
        daily = t.groupby(t["trade_date"].dt.date).agg(
            net_pl=("net_pl", "sum"),
            gross_pl=("gross_pl", "sum"),
            fees=("commissions_fees", "sum"),
            trades=("id", "count"),
        ).reset_index().rename(columns={"trade_date": "date"})
        daily["date"] = pd.to_datetime(daily["date"])
        st.line_chart(daily.set_index("date")[["net_pl"]])
        with st.expander("Daily breakdown table"):
            st.dataframe(daily, use_container_width=True)
    else:
        st.info("No trades loaded for the selected import.")

    st.divider()
    st.subheader("YTD + quarterly planning")
    year = int(selected_month.split("-")[0])
    ytd = get_ytd_summary(DB_PATH, year)
    ytd_tax = estimate_taxes(ytd.profit_after_costs, effective_tax_rate, set_aside_buffer)

    y1, y2, y3, y4, y5 = st.columns(5)
    y1.metric("YTD Gross P&L", f"{ytd.gross_pl:,.2f}")
    y2.metric("YTD Direct fees", f"{ytd.direct_fees:,.2f}")
    y3.metric("YTD Net P&L", f"{ytd.net_pl:,.2f}")
    y4.metric("YTD Overhead", f"{ytd.overhead_expenses:,.2f}")
    y5.metric("YTD Profit after costs", f"{ytd.profit_after_costs:,.2f}")

    y6, y7, y8 = st.columns(3)
    y6.metric("Est. tax (YTD)", f"{ytd_tax.est_tax:,.2f}")
    y7.metric("Set-aside target (YTD)", f"{ytd_tax.set_aside_target:,.2f}")
    y8.metric("After-tax profit (YTD)", f"{ytd_tax.est_after_tax_profit:,.2f}")

    q_profits = quarterly_profit_after_costs(DB_PATH, year)
    q_est = quarterly_estimates(q_profits, effective_tax_rate, set_aside_buffer)
    q_rows = []
    for q in ["Q1", "Q2", "Q3", "Q4"]:
        te = q_est.get(q)
        q_rows.append(
            {
                "quarter": q,
                "profit_after_costs": q_profits.get(q, 0.0),
                "est_tax": te.est_tax if te else 0.0,
                "set_aside_target": te.set_aside_target if te else 0.0,
                "after_tax_profit": te.est_after_tax_profit if te else 0.0,
            }
        )
    st.dataframe(pd.DataFrame(q_rows), use_container_width=True)

with tab_exp:
    st.subheader(f"Expenses — {selected_month}")
    st.caption(
        "Guardrail: Do not enter commissions/execution fees here. "
        "Your broker Net P&L already includes Commissions_Fees; duplicating them here risks double counting."
    )

    with st.form("add_expense"):
        c1, c2, c3 = st.columns(3)
        date = c1.text_input("Date (YYYY-MM-DD)", value=f"{selected_month}-01")
        vendor = c2.text_input("Vendor", value="Sierra Chart")
        category = c3.selectbox(
            "Category",
            [
                "platform_software",
                "market_data",
                "analytics_research",
                "internet_phone",
                "cloud_it_security",
                "professional_fees",
                "office_supplies",
                "home_office",
                "bank_fees",
                "education",
            ],
        )
        c4, c5, c6 = st.columns(3)
        amount = c4.number_input("Amount", min_value=0.0, value=40.0, step=1.0)
        business_use_pct = c5.slider("Business use %", 0.0, 1.0, 1.0, 0.05)
        memo = c6.text_input("Memo", value="Monthly subscription")
        deductible = float(amount) * float(business_use_pct)
        st.caption(f"Allocated deductible (planning): {deductible:,.2f}")

        if st.form_submit_button("Add expense"):
            validate_expense_category(category)
            conn.execute(
                "INSERT INTO expenses(date, vendor, category, amount, business_use_pct, memo) VALUES (?,?,?,?,?,?)",
                (date, vendor, category, float(amount), float(business_use_pct), memo),
            )
            conn.commit()
            st.success("Expense added.")

    exp = load_df(conn, "SELECT * FROM expenses WHERE substr(date,1,7)=? ORDER BY date ASC", (selected_month,))
    st.dataframe(exp, use_container_width=True)

with tab_assets:
    st.subheader(f"Assets — {selected_month}")
    with st.form("add_asset"):
        c1, c2, c3 = st.columns(3)
        description = c1.text_input("Description", value="Trading workstation")
        cost = c2.number_input("Cost", min_value=0.0, value=2500.0, step=50.0)
        placed = c3.text_input("Placed in service date (YYYY-MM-DD)", value=f"{selected_month}-15")
        c4, c5 = st.columns(2)
        biz = c4.slider("Business use %", 0.0, 1.0, 1.0, 0.05)
        method = c5.selectbox("Method (planning)", ["179", "depreciate"])

        if st.form_submit_button("Add asset"):
            conn.execute(
                "INSERT INTO assets(description, cost, placed_in_service_date, business_use_pct, method) VALUES (?,?,?,?,?)",
                (description, float(cost), placed, float(biz), method),
            )
            conn.commit()
            st.success("Asset added.")

    assets = load_df(conn, "SELECT * FROM assets WHERE substr(placed_in_service_date,1,7)=? ORDER BY placed_in_service_date ASC", (selected_month,))
    st.dataframe(assets, use_container_width=True)

with tab_exports:
    st.subheader(f"Exports — {selected_month}")
    ok = export_readiness(conn, selected_month)
    with st.expander("What gets exported"):
        st.markdown(
            "- monthly summary (after costs + planning taxes)\n"
            "- expenses (allocated)\n"
            "- assets\n"
            "- reconciliation report\n"
        )

    if st.button("Export monthly bundle", disabled=not ok):
        try:
            base = export_monthly_bundle(DB_PATH, selected_month, EXPORT_DIR, effective_tax_rate, set_aside_buffer)
            st.success(f"Exported: {base.name}.*.csv in {EXPORT_DIR}")
        except Exception as e:
            st.error(str(e))

    st.caption(f"Exports folder: {EXPORT_DIR.resolve()}")

conn.close()
