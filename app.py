# National Student Tracker - Streamlit Version

import streamlit as st
import pandas as pd
import numpy as np
import folium
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# ---- Page Setup ----
st.set_page_config(page_title="National Student Tracker", layout="wide")
st.title("📍 National Student Tracker")

# ---- Load Data ----
if 'data' not in st.session_state:
    np.random.seed(42)
    st.session_state.data = pd.DataFrame({
        'id': range(1, 101),
        'lat': np.random.uniform(34, 38, 100),
        'lng': np.random.uniform(-120, -115, 100),
        'region': np.random.choice(['Region 1', 'Region 2', 'Region 3'], 100),
        'GPA': np.random.uniform(2.0, 4.0, 100),
        'age': np.random.randint(17, 25, 100),
        'address': ['123 Example St, CA'] * 100
    })

uploaded_file = st.sidebar.file_uploader("Upload your CSV data", type=["csv"])
if uploaded_file is not None:
    st.session_state.data = pd.read_csv(uploaded_file)

data = st.session_state.data

# ---- Add Simulated Fields ----
if 'interest' not in data.columns:
    data['interest'] = np.random.choice(['STEM', 'Arts', 'Business', 'Health', 'Engineering'], size=len(data))
    data['likely_university'] = np.random.choice(['State University', 'Community College', 'Tech Institute', 'Liberal Arts College'], size=len(data))
    data['high_school'] = np.random.choice(['Lincoln HS', 'Jefferson HS', 'Washington HS'], size=len(data))

# ---- Enrollment Likelihood ----
st.subheader("📈 Enrollment Likelihood Score")
def calculate_likelihood(gpa, age):
    score = (gpa - 2.0) / 2.0 * 50 + (25 - abs(age - 18))
    return round(min(max(score, 0), 100), 1)

data['enrollment_likelihood'] = data.apply(lambda row: calculate_likelihood(row['GPA'], row['age']), axis=1)

# ---- Filter Sidebar ----
region_choice = st.sidebar.selectbox("Select Region:", ["All"] + sorted(data['region'].unique()))
if region_choice != "All":
    data = data[data['region'] == region_choice]

# ---- Score Filter ----
st.subheader("🎯 Filter by Enrollment Likelihood")
min_score, max_score = int(data['enrollment_likelihood'].min()), int(data['enrollment_likelihood'].max())
score_range = st.sidebar.slider("Enrollment Likelihood Range", min_score, max_score, (min_score, max_score))
data = data[(data['enrollment_likelihood'] >= score_range[0]) & (data['enrollment_likelihood'] <= score_range[1])]

# ---- Summary Table ----
st.subheader("📊 Summary Table by Region")
st.dataframe(data.groupby("region").size().reset_index(name="Count"))

# ---- Bar Chart ----
region_counts = data['region'].value_counts()
fig1, ax1 = plt.subplots()
region_counts.plot(kind='bar', ax=ax1, color='skyblue')
ax1.set_title("Students by Region")
st.pyplot(fig1)

# ---- Pie Chart ----
fig2, ax2 = plt.subplots()
region_counts.plot(kind='pie', ax=ax2, autopct='%1.1f%%')
ax2.set_ylabel('')
ax2.set_title("Region Distribution")
st.pyplot(fig2)

# ---- Student Map ----
st.subheader("🗺️ Student Locations by Likelihood")
try:
    import streamlit_folium as sf
    m = folium.Map(location=[36, -118], zoom_start=6)
    for _, row in data.iterrows():
        color = "green" if row['enrollment_likelihood'] > 75 else "orange" if row['enrollment_likelihood'] > 50 else "red"
        folium.CircleMarker(
            location=[row['lat'], row['lng']],
            radius=5,
            color=color,
            fill=True,
            popup=f"ID: {row['id']} | Score: {row['enrollment_likelihood']}"
        ).add_to(m)
    sf.st_folium(m, width=700, height=450)
except:
    st.error("Map cannot be displayed because folium/streamlit-folium is not supported in this environment.")

# ---- Predictive Modeling ----
st.subheader("🤖 Predictive Modeling")
try:
    features = ['GPA', 'age', 'lat', 'lng']
    data = pd.get_dummies(data, columns=['interest', 'likely_university', 'high_school'])
    features += [col for col in data.columns if col.startswith('interest_') or col.startswith('likely_university_') or col.startswith('high_school_')]
    X = data[features].dropna()
    y = np.random.randint(1, 100, size=len(X))
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    importances = model.feature_importances_
    importance_df = pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values(by='Importance', ascending=False)
    st.metric("Model R²", f"{score:.2f}")
    st.dataframe(importance_df)
    fig_imp, ax_imp = plt.subplots()
    sns.barplot(data=importance_df.head(10), x='Importance', y='Feature', ax=ax_imp)
    ax_imp.set_title("Top 10 Feature Importances")
    st.pyplot(fig_imp)
except Exception as e:
    st.error(f"Modeling failed: {e}")

# ---- Top Students Preview ----
st.subheader("🔍 Top Enrollment Candidates")
st.dataframe(data.sort_values(by='enrollment_likelihood', ascending=False)[['id', 'region', 'GPA', 'age', 'enrollment_likelihood']].head(10))
