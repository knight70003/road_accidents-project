import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# ---- MySQL Connection ----
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='RC'
)

# ---- Fetch Data from MySQL ----
query = "SELECT * FROM road_accidents"
df = pd.read_sql(query, connection)
connection.close()

# ---- Dashboard UI ----
st.title("Road Accidents Dashboard")

# ---- Filters ----

filtered_df = df.copy()

# Filter Cities
selected_cities = st.multiselect(
    "Select Cities",
    df['Million Plus Cities'].dropna().unique()
)
if selected_cities:
    filtered_df = filtered_df[filtered_df['Million Plus Cities'].isin(selected_cities)]

# Filter Causes
selected_causes = st.multiselect(
    "Select Causes",
    df['Cause category'].dropna().unique()
)
if selected_causes:
    filtered_df = filtered_df[filtered_df['Cause category'].isin(selected_causes)]

# Filter Cause Subcategories
selected_subcategories = st.multiselect(
    "Select Cause Subcategories",
    df['Cause Subcategory'].dropna().unique()
)
if selected_subcategories:
    filtered_df = filtered_df[filtered_df['Cause Subcategory'].isin(selected_subcategories)]


# ---- Charts ----

# Chart 1: Severity Distribution
st.subheader("Accident Severity Distribution")
fig1 = px.histogram(
    filtered_df,
    x='Outcome of Incident',
    color="Outcome of Incident",
    title='Accidents Severity Distribution'
)
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Fatalities by City
st.subheader("Fatalities by City")
fig2 = px.bar(
    filtered_df,
    x='Million Plus Cities',
    y='Count',
    color='Outcome of Incident',
    title='Count by City'
)
st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Causes of Accidents
st.subheader("Causes of Accidents")
fig3 = px.pie(
    filtered_df,
    names='Cause category',
    title='Causes of Accidents'
)
st.plotly_chart(fig3, use_container_width=True)