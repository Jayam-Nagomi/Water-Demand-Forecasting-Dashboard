import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Page Configuration ----
st.set_page_config(page_title="Reservoir Level", layout="wide")

# ---- Load Data ----
df = pd.read_csv("Data.csv", parse_dates=["date"])

# Create a clipped column for metrics
dead_storage_threshold = 0.05
df["Reservoir_clipped"] = df["Reservoir"].apply(
    lambda x: dead_storage_threshold if x < dead_storage_threshold else x
)

# ---- Sidebar Configuration ----
st.sidebar.title("Reservoir Storage Analysis")

# Multi-Select for Months
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
month_map = {m: i+1 for i, m in enumerate(months)}

selected_months = st.sidebar.multiselect(
    "Select Months",
    options=months,
    default=months  
)

# Filter Data Based on Selected Months
df["month_num"] = df["date"].dt.month
if selected_months:
    selected_month_nums = [month_map[m] for m in selected_months]
    df_filtered = df[df["month_num"].isin(selected_month_nums)].copy()
else:
    df_filtered = pd.DataFrame()  

# ---- Metrics (using clipped column) ----
st.title("Reservoir Levels Overview")

col1, col2, col3 = st.columns(3)
if not df_filtered.empty:
    col1.metric(
        "Average Storage (%)",  
        f"{df_filtered['Reservoir_clipped'].mean():.2f}"
    )
    col2.metric(
        "Lowest Level (%)", 
        f"{df_filtered['Reservoir_clipped'].min():.2f}",
        f"{df_filtered.loc[df_filtered['Reservoir_clipped'].idxmin(), 'date'].date()}"
    )
    col3.metric(
        "Highest Level (%)", 
        f"{df_filtered['Reservoir_clipped'].max():.2f}",
        f"{df_filtered.loc[df_filtered['Reservoir_clipped'].idxmax(), 'date'].date()}"
    )
else:
    col1.metric("Average Storage (%)", "N/A")
    col2.metric("Lowest Level (%)", "N/A")
    col3.metric("Highest Level (%)", "N/A")

# ---- Charts ----
if not df_filtered.empty:
    # 1. Time-Series Line Chart
    fig1 = px.line(
        df_filtered,
        x="date",
        y="Reservoir",
        labels={"Reservoir": "Reservoir Level (%)"},
        title="Daily Reservoir Storage Trends"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Monthly Summary Bar Chart
    df_filtered["month_str"] = df_filtered["date"].dt.strftime("%b")
    monthly_summary = (
        df_filtered.groupby("month_str")["Reservoir"]
        .mean()
        .reset_index()
        .assign(month_num=lambda d: d["month_str"].map({v:k for k,v in month_map.items()}))
        .sort_values("month_num")
    )

    fig2 = px.bar(
        monthly_summary,
        x="month_str",
        y="Reservoir",
        labels={"Reservoir": "Average Reservoir Level (%)", "month_str": "Month"},
        title="Monthly Average Reservoir Storage"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Box Plot for Variability
    fig3 = px.box(
        df_filtered,
        x="month_str",
        y="Reservoir",
        labels={"Reservoir": "Reservoir Level (%)", "month_str": "Month"},
        title="Reservoir Level Distribution by Month"
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("No data available for the selected month(s).")

# ---- Footer ----
st.divider()
def create_footer():
    footer_html = """
    <div style='text-align: center; padding: 10px; font-size: 0.9em; color: #888;'>
        <p>Disclaimer: This data is based on 2023 records and may not reflect real-time changes.</p>
        <p>Author: Nagomi Jayamani (2025)</p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

create_footer()
