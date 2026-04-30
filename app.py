import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

st.set_page_config(
    page_title="Support Team Performance Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Support Team Performance Dashboard")
st.markdown("Track advisor performance, resolution times, CSAT scores, and escalations.")

# ── Data loading ──────────────────────────────────────────────────────────────

@st.cache_data
def load_data(source):
    df = pd.read_csv(source)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

with st.sidebar:
    st.header("⚙️ Filters")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded:
    df = load_data(uploaded)
else:
    df = load_data("data/support_data.csv")
    st.sidebar.info("Using built-in sample data. Upload a CSV to use your own.")

# ── Sidebar filters ───────────────────────────────────────────────────────────

with st.sidebar:
    min_date, max_date = df["Date"].min().date(), df["Date"].max().date()
    date_range = st.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    advisors = st.multiselect("Advisor", options=sorted(df["Advisor Name"].unique()), default=sorted(df["Advisor Name"].unique()))

# Apply filters
if len(date_range) == 2:
    start, end = date_range
    df = df[(df["Date"].dt.date >= start) & (df["Date"].dt.date <= end)]

if advisors:
    df = df[df["Advisor Name"].isin(advisors)]

if df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# ── KPI metrics ───────────────────────────────────────────────────────────────

st.subheader("Key Metrics")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Cases", int(df["Cases Handled"].sum()))
k2.metric("Avg Resolution Time", f"{df['Avg Resolution Time (min)'].mean():.1f} min")
k3.metric("Avg CSAT Score", f"{df['CSAT Score'].mean():.2f} / 5.0")
k4.metric("Total Escalations", int(df["Escalations"].sum()))

st.divider()

# ── Charts ────────────────────────────────────────────────────────────────────

col1, col2 = st.columns(2)

with col1:
    st.subheader("CSAT Score Over Time")
    csat_trend = df.groupby(["Date", "Advisor Name"])["CSAT Score"].mean().reset_index()
    fig_line = px.line(
        csat_trend,
        x="Date",
        y="CSAT Score",
        color="Advisor Name",
        markers=True,
        range_y=[3.5, 5.2],
    )
    fig_line.update_layout(margin=dict(t=20, b=20), legend_title="Advisor")
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.subheader("Cases Handled per Advisor")
    cases_by_advisor = df.groupby("Advisor Name")["Cases Handled"].sum().reset_index().sort_values("Cases Handled", ascending=False)
    fig_bar = px.bar(
        cases_by_advisor,
        x="Advisor Name",
        y="Cases Handled",
        color="Advisor Name",
        text="Cases Handled",
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(margin=dict(t=20, b=20), showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Escalation Breakdown by Category")
    esc_df = df[df["Escalation Category"] != "None"]
    if esc_df.empty:
        st.info("No escalations in selected range.")
    else:
        esc_counts = esc_df["Escalation Category"].value_counts().reset_index()
        esc_counts.columns = ["Category", "Count"]
        fig_pie = px.pie(esc_counts, names="Category", values="Count", hole=0.4)
        fig_pie.update_layout(margin=dict(t=20, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

with col4:
    st.subheader("Avg Resolution Time per Advisor")
    res_time = df.groupby("Advisor Name")["Avg Resolution Time (min)"].mean().reset_index().sort_values("Avg Resolution Time (min)")
    fig_res = px.bar(
        res_time,
        x="Avg Resolution Time (min)",
        y="Advisor Name",
        orientation="h",
        color="Avg Resolution Time (min)",
        color_continuous_scale="RdYlGn_r",
        text=res_time["Avg Resolution Time (min)"].round(1),
    )
    fig_res.update_traces(textposition="outside")
    fig_res.update_layout(margin=dict(t=20, b=20), coloraxis_showscale=False)
    st.plotly_chart(fig_res, use_container_width=True)

# ── Raw data table ────────────────────────────────────────────────────────────

with st.expander("📋 View Raw Data"):
    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Filtered CSV", csv, "filtered_support_data.csv", "text/csv")
