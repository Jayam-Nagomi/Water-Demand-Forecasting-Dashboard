import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Page Configuration ----
st.set_page_config(page_title="Home", layout="wide")

# ---- Load Data ----
df = pd.read_csv("Data.csv", parse_dates=["date"])

# ---- Create day_of_year & label dict ----
df["day_of_year"] = df["date"].dt.dayofyear
dayofyear_to_label = {}
for doy in df["day_of_year"].unique():
    date_label = df.loc[df["day_of_year"] == doy, "date"].iloc[0].strftime("%b %d")
    dayofyear_to_label[doy] = date_label

# ---- Clip Reservoir Values for Metrics Only ----
dead_storage_threshold = 0.05
df["Reservoir_clipped"] = df["Reservoir"].apply(
    lambda x: dead_storage_threshold if x < dead_storage_threshold else x
)

# ---- Sidebar Configuration ----
st.sidebar.title("Home")

# Create a sorted list of all possible day_of_year values
all_days = sorted(df["day_of_year"].unique())

# Slider
start_doy, end_doy = st.sidebar.select_slider(
    label="Select Month-Day Range",
    options=all_days,                  
    value=(all_days[0], all_days[-1]), 
    format_func=lambda x: dayofyear_to_label.get(x, f"Day {x}")
)

# Filter Data
df_filtered = df[
    (df["day_of_year"] >= start_doy) & 
    (df["day_of_year"] <= end_doy)
].copy()

# ---- Metrics ----
st.title("Water Demand Forecasting Dashboard")

col1, col2, col3 = st.columns(3)

if not df_filtered.empty:
    col1.metric(
        "Avg Reservoir Level (%)",
        f"{df_filtered['Reservoir_clipped'].mean():.2f}"
    )
    col2.metric(
        "Avg Groundwater Level (m)",
        f"{df_filtered['GW Level'].mean():.2f}"
    )
    col3.metric(
        "Avg Rainfall (mm)",
        f"{df_filtered['Rainfall'].mean():.2f}"
    )
else:
    col1.metric("Avg Reservoir Level (%)", "No data")
    col2.metric("Avg Groundwater Level (m)", "No data")
    col3.metric("Avg Rainfall (mm)", "No data")

# ---- Overview Chart ----
if not df_filtered.empty:
    fig = px.line(
        df_filtered,
        x="date",
        y=["Reservoir", "GW Level", "Rainfall"],  # raw data for charts
        labels={"value": "Measurement", "variable": "Category", "date": "Date"},
        title="Water Data Overview"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for the selected month-day range.")

# ---- Feedback Section ----
if "feedback_submitted" not in st.session_state:
    st.session_state["feedback_submitted"] = False

def feedback_submitted():
    st.session_state["feedback_submitted"] = True

st.markdown("<h3 style='text-align: center;'>How much do you like the dashboard?</h3>", unsafe_allow_html=True)
col_a, col_b, col_c, col_d = st.columns([1,1,2,1])
with col_c:
    st.feedback("stars", on_change=feedback_submitted)

if st.session_state["feedback_submitted"]:
    st.toast("Thanks for your feedback! 🎉")
    st.session_state["feedback_submitted"] = False

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
