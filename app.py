import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page Configuration
st.set_page_config(
    page_title="Oil & Gas Production Dashboard",
    page_icon="🛢️",
    layout="wide"
)

# Title
st.title("Oil & Gas Production Dashboard")

# Generate or Load Data
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    """Loads production data from CSV or generates new data if missing."""
    data_path = "data/production_data.csv"
    
    if not os.path.exists(data_path):
        from src.data_generator import generate_production_data  # Import only when needed
        df = generate_production_data()
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path, parse_dates=['date'])
    
    return df

data = load_data()

# Sidebar Filters
st.sidebar.header("Filters")

well_options = data['well_id'].unique()
default_wells = well_options[:3] if len(well_options) >= 3 else well_options

well_selection = st.sidebar.multiselect(
    "Select Wells",
    options=well_options,
    default=default_wells
)

# Filter Data Based on Selection
filtered_data = data[data['well_id'].isin(well_selection)]

# Layout Setup
col1, col2 = st.columns(2)

# Oil Production Trend
with col1:
    st.subheader("Oil Production Over Time")
    fig_oil = px.line(
        filtered_data,
        x='date',
        y='oil_production',
        color='well_id',
        title='Oil Production Over Time'
    )
    st.plotly_chart(fig_oil, use_container_width=True)

# Gas Production Trend
with col2:
    st.subheader("Gas Production Over Time")
    fig_gas = px.line(
        filtered_data,
        x='date',
        y='gas_production',
        color='well_id',
        title='Gas Production Over Time'
    )
    st.plotly_chart(fig_gas, use_container_width=True)

# Production Metrics Section
st.header("Production Metrics")

col3, col4, col5 = st.columns(3)

with col3:
    total_oil = filtered_data['oil_production'].sum()
    st.metric("Total Oil Production", f"{total_oil:,.0f} BBL")

with col4:
    total_gas = filtered_data['gas_production'].sum()
    st.metric("Total Gas Production", f"{total_gas:,.0f} MCF")

with col5:
    total_water = filtered_data['water_production'].sum()
    st.metric("Total Water Production", f"{total_water:,.0f} BBL")
