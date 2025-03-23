import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Page Configuration ----
st.set_page_config(page_title="Groundwater Insights", layout="wide")

# ---- Load Data ----
df = pd.read_csv("Data.csv", parse_dates=["date"])

# ---- Sidebar Configuration ----
st.sidebar.title("Groundwater Analysis")

# Month Range Slider
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

st.sidebar.write("Select Month Range")
selected_month_range = st.sidebar.select_slider(
    " ",
    options=months,  
    value=("Jan", "Dec")  
)

month_to_num = {month: i + 1 for i, month in enumerate(months)}

start_month = month_to_num[selected_month_range[0]]
end_month = month_to_num[selected_month_range[1]]

df["month"] = df["date"].dt.month 

# Filter Data
df_filtered = df[(df["month"] >= start_month) & (df["month"] <= end_month)]

# ---- Metrics ----
st.title("Groundwater Insights")

col1, col2, col3 = st.columns(3)
col1.metric("Average GW Level (m)", f"{df_filtered['GW Level'].mean():.2f}")
col2.metric("Lowest Level (m)", f"{df_filtered['GW Level'].min():.2f}", 
            f"{df_filtered.loc[df_filtered['GW Level'].idxmin(), 'date'].date()}")
col3.metric("Highest Level (m)", f"{df_filtered['GW Level'].max():.2f}", 
            f"{df_filtered.loc[df_filtered['GW Level'].idxmax(), 'date'].date()}")

# ---- Charts ----

# Daily Groundwater Fluctuations 
fig1 = px.line(
    df_filtered.sort_values("date"),  
    x="date",
    y="GW Level",
    labels={"date": "Date", "GW Level": "Groundwater Level (m)"},
    title="Daily Groundwater Fluctuations"
)
st.plotly_chart(fig1, use_container_width=True)

# Seasonal Heatmap
df["day"] = df["date"].dt.day
df["month_name"] = df["date"].dt.strftime("%b")

heatmap_data = df.pivot_table(index="day", columns="month_name", values="GW Level")

fig2 = px.imshow(
    heatmap_data,
    labels={"color": "GW Level (m)"},
    title="Seasonal Groundwater Variability",
    color_continuous_scale="blues"
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
