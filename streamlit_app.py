%%writefile app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Global Modern Crises Dashboard",
    page_icon="🌍",
    layout="wide"
)

# =====================================
# LOAD DATASET
# =====================================

@st.cache_data
def load_data():
    df = pd.read_excel("global_modern_crises.xlsx")
    df["Date Reported"] = pd.to_datetime(
        df["Date Reported"], errors="coerce"
    )
    return df

df = load_data()

# =====================================
# DASHBOARD TITLE
# =====================================

st.title("🌍 GLOBAL MODERN CRISES ANALYSIS")
st.markdown(
    "### Interactive Humanitarian Crisis Dashboard"
)
st.caption(
    "Explore global crises, fatalities, displacement "
    "and humanitarian funding gaps."
)

st.divider()

# =====================================
# SIDEBAR FILTERS
# =====================================

st.sidebar.title("Dashboard Filters")

if st.sidebar.button("Reset All Filters"):
    st.rerun()

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].dropna().unique())
)

countries = st.sidebar.multiselect(
    "Select Country",
    options=sorted(df["Country"].dropna().unique())
)

crisis_types = st.sidebar.multiselect(
    "Select Crisis Type",
    options=sorted(df["Crisis Type"].dropna().unique())
)

severity = st.sidebar.multiselect(
    "Select Severity Level",
    options=sorted(df["Severity Level"].dropna().unique())
)

# =====================================
# APPLY FILTERS
# =====================================

filtered_df = df.copy()

if regions:
    filtered_df = filtered_df[
        filtered_df["Region"].isin(regions)
    ]

if countries:
    filtered_df = filtered_df[
        filtered_df["Country"].isin(countries)
    ]

if crisis_types:
    filtered_df = filtered_df[
        filtered_df["Crisis Type"].isin(crisis_types)
    ]

if severity:
    filtered_df = filtered_df[
        filtered_df["Severity Level"].isin(severity)
    ]

# =====================================
# KPI CALCULATIONS
# =====================================

total_crises = filtered_df["Crisis ID"].nunique()

total_fatalities = filtered_df[
    "Estimated Fatalities"
].sum()

total_displaced = filtered_df[
    "Individuals Displaced"
].sum()

total_funding_gap = filtered_df[
    "Funding Gap ($)"
].sum()

avg_funded = filtered_df[
    "Percentage Funded (%)"
].mean()

# =====================================
# KPI CARDS
# =====================================

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Crises",
    f"{total_crises:,}"
)

col2.metric(
    "Total Fatalities",
    f"{total_fatalities:,.0f}"
)

col3.metric(
    "People Displaced",
    f"{total_displaced:,.0f}"
)

col4.metric(
    "Funding Gap",
    f"${total_funding_gap:,.0f}"
)

col5.metric(
    "Average Funded",
    f"{avg_funded:.2f}%" if pd.notna(avg_funded) else "N/A"
)

st.divider()

# =====================================
# CHART 1: CRISIS TYPE DISTRIBUTION
# =====================================

st.subheader("1. Distribution of Crisis Types")

crisis_data = (
    filtered_df.groupby("Crisis Type")["Crisis ID"]
    .nunique()
    .reset_index(name="Total Crises")
)

fig1 = px.pie(
    crisis_data,
    names="Crisis Type",
    values="Total Crises",
    hole=0.45,
    title="Distribution of Crisis Types"
)

st.plotly_chart(fig1, use_container_width=True)

# =====================================
# CHART 2: FATALITY TREND
# =====================================

st.subheader("2. Fatality Trend Over Time")

trend_data = (
    filtered_df.dropna(subset=["Date Reported"])
    .groupby("Date Reported")["Estimated Fatalities"]
    .sum()
    .reset_index()
)

fig2 = px.line(
    trend_data,
    x="Date Reported",
    y="Estimated Fatalities",
    markers=True,
    title="Fatalities Over Time"
)

st.plotly_chart(fig2, use_container_width=True)

# =====================================
# CHART 3: FUNDING GAP BY REGION
# =====================================

st.subheader("3. Funding Gap by Region")

funding_data = (
    filtered_df.groupby("Region")["Funding Gap ($)"]
    .sum()
    .reset_index()
    .sort_values("Funding Gap ($)", ascending=False)
)

fig3 = px.bar(
    funding_data,
    x="Region",
    y="Funding Gap ($)",
    color="Region",
    title="Funding Gap by Region"
)

st.plotly_chart(fig3, use_container_width=True)

# =====================================
# CHART 4: TOP 10 COUNTRIES BY DISPLACEMENT
# =====================================

st.subheader("4. Top 10 Countries by Displacement")

top_countries = (
    filtered_df.groupby("Country")["Individuals Displaced"]
    .sum()
    .nlargest(10)
    .reset_index()
)

fig4 = px.bar(
    top_countries,
    x="Individuals Displaced",
    y="Country",
    orientation="h",
    title="Top 10 Countries by Displaced Population"
)

fig4.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig4, use_container_width=True)

# =====================================
# CHART 5: SEVERITY LEVEL
# =====================================

st.subheader("5. Crisis Severity Analysis")

severity_data = (
    filtered_df.groupby("Severity Level")["Crisis ID"]
    .nunique()
    .reset_index(name="Total Crises")
)

fig5 = px.bar(
    severity_data,
    x="Severity Level",
    y="Total Crises",
    color="Severity Level",
    title="Crises by Severity Level"
)

st.plotly_chart(fig5, use_container_width=True)

# =====================================
# CHART 6: FATALITIES BY CRISIS TYPE
# =====================================

st.subheader("6. Fatalities by Crisis Type")

fatality_data = (
    filtered_df.groupby("Crisis Type")["Estimated Fatalities"]
    .sum()
    .reset_index()
    .sort_values("Estimated Fatalities", ascending=False)
)

fig6 = px.bar(
    fatality_data,
    x="Crisis Type",
    y="Estimated Fatalities",
    title="Fatalities by Crisis Type"
)

st.plotly_chart(fig6, use_container_width=True)

# =====================================
# FILTERED DATA TABLE
# =====================================

st.divider()

with st.expander("View Filtered Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# =====================================
# FOOTER
# =====================================

st.divider()

st.markdown(
    "**Global Modern Crises Analysis Dashboard**"
)

st.caption(
    "Developed using Python, Pandas, Plotly and Streamlit."
)
