
# National Student Tracker - Matplotlib Console-Compatible Version

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# ---- Load Data ----
np.random.seed(42)
data = pd.DataFrame({
    'id': range(1, 101),
    'lat': np.random.uniform(34, 38, 100),
    'lng': np.random.uniform(-120, -115, 100),
    'region': np.random.choice(['Region 1', 'Region 2', 'Region 3'], 100),
    'GPA': np.random.uniform(2.0, 4.0, 100),
    'age': np.random.randint(17, 25, 100),
    'address': ['123 Example St, CA'] * 100
})

# ---- Add Simulated Fields ----
data['interest'] = np.random.choice(['STEM', 'Arts', 'Business', 'Health', 'Engineering'], size=len(data))
data['likely_university'] = np.random.choice(['State University', 'Community College', 'Tech Institute', 'Liberal Arts College'], size=len(data))
data['high_school'] = np.random.choice(['Lincoln HS', 'Jefferson HS', 'Washington HS'], size=len(data))

# ---- Enrollment Likelihood ----
def calculate_likelihood(gpa, age):
    score = (gpa - 2.0) / 2.0 * 50 + (25 - abs(age - 18))
    return round(min(max(score, 0), 100), 1)

data['enrollment_likelihood'] = data.apply(lambda row: calculate_likelihood(row['GPA'], row['age']), axis=1)

# ---- Summary Table by Region ----
print("\n📊 Summary Table by Region")
print(data.groupby("region").size().reset_index(name="Count"))

# ---- Bar Chart: Students by Region ----
region_counts = data['region'].value_counts()
fig1, ax1 = plt.subplots()
region_counts.plot(kind='bar', ax=ax1, color='skyblue')
ax1.set_title("Students by Region")
plt.tight_layout()
plt.show()

# ---- Pie Chart: Region Distribution ----
fig2, ax2 = plt.subplots()
region_counts.plot(kind='pie', ax=ax2, autopct='%1.1f%%')
ax2.set_ylabel('')
ax2.set_title("Region Distribution")
plt.tight_layout()
plt.show()

# ---- Predictive Modeling ----
print("\n🤖 Predictive Modeling")
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

print(f"Model R²: {score:.2f}")

importances = model.feature_importances_
importance_df = pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values(by='Importance', ascending=False)
print("\nFeature Importances:")
print(importance_df.head(10))

fig_imp, ax_imp = plt.subplots()
sns.barplot(data=importance_df.head(10), x='Importance', y='Feature', ax=ax_imp)
ax_imp.set_title("Top 10 Feature Importances")
plt.tight_layout()
plt.show()

# ---- Top Students Preview ----
print("\n🔍 Top Enrollment Candidates")
print(data.sort_values(by='enrollment_likelihood', ascending=False)[['id', 'region', 'GPA', 'age', 'enrollment_likelihood']].head(10))
