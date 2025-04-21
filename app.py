# National Student Tracker - Streamlit Version

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# ---- Page Setup ----
st.set_page_config(page_title="National Student Tracker", layout="wide")
st.title("\U0001F4CD National Student Tracker")

# ---- File Upload ----
uploaded_file = st.sidebar.file_uploader("Upload your CSV data", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    np.random.seed(42)
    data = pd.DataFrame({
        'id': range(1, 101),
        'lat': np.random.uniform(34, 38, 100),
        'lng': np.random.uniform(-120, -115, 100),
        'region': np.random.choice(['Region 1', 'Region 2', 'Region 3'], 100)
    })

# ---- Sidebar Filters ----
region_choice = st.sidebar.selectbox("Select Region:", options=["All", "Region 1", "Region 2", "Region 3"])
date_range = st.sidebar.date_input("Select Date Range", value=(pd.to_datetime("2023-01-01"), pd.to_datetime("2023-12-31")))

# ---- Filter Logic ----
if region_choice != "All":
    data = data[data["region"] == region_choice]

# ---- Map ----
st.subheader("\U0001F5FA️ Map of Students")
m = folium.Map(location=[36, -118], zoom_start=6)
for _, row in data.iterrows():
    folium.CircleMarker(
        location=(row["lat"], row["lng"]),
        radius=5,
        popup=f"ID: {row['id']} - {row['region']}",
        color="blue",
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

st_folium(m, width=700, height=450)

# ---- Summary Table ----
st.subheader("\U0001F4CA Summary Table by Region")
summary = data.groupby("region").size().reset_index(name="Count")
st.dataframe(summary)
