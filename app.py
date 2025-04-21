import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="National Student Tracker", layout="wide")
st.title("📍 National Student Tracker")

# Load data
data = pd.read_csv("sample_students.csv")

region_choice = st.sidebar.selectbox("Select Region:", options=["All"] + list(data["region"].unique()))
date_range = st.sidebar.date_input("Select Date Range", value=(pd.to_datetime("2023-01-01"), pd.to_datetime("2023-12-31")))

if region_choice != "All":
    data = data[data["region"] == region_choice]

st.subheader("🗺️ Map of Students")
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

st.subheader("📊 Summary Table by Region")
summary = data.groupby("region").size().reset_index(name="Count")
st.dataframe(summary)
