import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Page Configuration ----
st.set_page_config(page_title="Rainfall Patterns", layout="wide")

# ---- Load Data ----
df = pd.read_csv("Data.csv", parse_dates=["date"])

df["quarter"] = df["date"].dt.quarter
df["month_num"] = df["date"].dt.month
df["month_str"] = df["date"].dt.strftime("%b")

# ---- Sidebar: Quarter Selection ----
st.sidebar.title("Rainfall Analysis")
quarter_selection = st.sidebar.pills(
    label="Select Quarter(s)",
    options=[1, 2, 3, 4],         
    selection_mode="multi",       
    default=[1, 2, 3, 4],          
    format_func=lambda q: f"Q{q}", 
)

# Filter data for selected quarters
df_filtered = df[df["quarter"].isin(quarter_selection)]

if not quarter_selection or df_filtered.empty:
    st.warning("Select atleast one quarter!")
else:
    # ---- Metrics ----
    st.title("Rainfall Patterns Overview")

    total_rainfall = df_filtered["Rainfall"].sum()

    monthly_data = (
        df_filtered.groupby(["month_num", "month_str"])["Rainfall"]
        .sum()
        .reset_index()
        .sort_values("month_num")
    )

    wettest_idx = monthly_data["Rainfall"].idxmax()
    driest_idx = monthly_data["Rainfall"].idxmin()

    wettest_month = monthly_data.loc[wettest_idx, "month_str"]
    wettest_val = monthly_data.loc[wettest_idx, "Rainfall"]
    driest_month = monthly_data.loc[driest_idx, "month_str"]
    driest_val = monthly_data.loc[driest_idx, "Rainfall"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rainfall (mm)", f"{total_rainfall:.2f}")
    col2.metric("Wettest Month", f"{wettest_month}", f"{wettest_val:.2f} mm")
    col3.metric("Driest Month", f"{driest_month}", f"{driest_val:.2f} mm")

    # ---- Charts ----
    # 1. Daily Rainfall
    fig1 = px.line(
        df_filtered,
        x="date",
        y="Rainfall",
        labels={"date": "Date", "Rainfall": "Rainfall (mm)"},
        title="Daily Rainfall"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Monthly Rainfall Distribution
    fig2 = px.area(
        monthly_data,
        x="month_str",
        y="Rainfall",
        labels={"month_str": "Month", "Rainfall": "Total Rainfall (mm)"},
        title="Rainfall by Month"
    )
    st.plotly_chart(fig2, use_container_width=True)

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
