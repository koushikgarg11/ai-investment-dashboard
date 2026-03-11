import streamlit as st
import pandas as pd

from modules.data_loader import load_macro_data
from modules.kpi_engine import calculate_investment_score
from modules.visualization import country_comparison, investment_heatmap
from modules.recommendation import get_recommendations
from modules.report_generator import generate_pdf_report


st.set_page_config(
    page_title="AI Global Investment Intelligence Platform",
    layout="wide"
)

st.title("🌎 AI Global Investment Intelligence Platform")

st.write(
"""
Analyze global investment opportunities using macroeconomic indicators.
Compare countries, explore investment attractiveness, and generate reports.
"""
)

# ===============================
# LOAD DATA
# ===============================

with st.spinner("Loading global economic data..."):
    df = load_macro_data()

if df is None or df.empty:
    st.error("Data could not be loaded.")
    st.stop()

# Calculate Investment Score
df = calculate_investment_score(df)

# ===============================
# SIDEBAR CONTROLS
# ===============================

st.sidebar.header("⚙️ Dashboard Controls")

countries = sorted(df["Country"].dropna().unique())

selected_country = st.sidebar.selectbox(
    "Select Country",
    countries
)

compare_countries = st.sidebar.multiselect(
    "Compare Countries",
    countries,
    default=[selected_country]
)

# ===============================
# FILTER DATA
# ===============================

country_data = df[df["Country"] == selected_country].iloc[-1]

# ===============================
# EXECUTIVE SUMMARY DASHBOARD
# ===============================

st.subheader("📊 Executive Summary Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "GDP",
    f"${country_data.get('GDP',0):,.0f}" if pd.notna(country_data.get("GDP")) else "N/A"
)

col2.metric(
    "Inflation (%)",
    f"{country_data.get('Inflation','N/A')}"
)

col3.metric(
    "Population",
    f"{country_data.get('Population',0):,.0f}" if pd.notna(country_data.get("Population")) else "N/A"
)

col4.metric(
    "Investment Score",
    round(country_data.get("Investment Score",0),2)
)

# ===============================
# COUNTRY COMPARISON
# ===============================

st.subheader("🌍 Country Comparison")

try:
    comparison_chart = country_comparison(df, compare_countries)
    st.plotly_chart(comparison_chart, use_container_width=True)
except:
    st.warning("Country comparison chart could not be generated.")

# ===============================
# GLOBAL INVESTMENT HEATMAP
# ===============================

st.subheader("🌎 Global Investment Attractiveness")

try:
    heatmap = investment_heatmap(df)
    st.plotly_chart(heatmap, use_container_width=True)
except:
    st.warning("Heatmap could not be generated.")

# ===============================
# INDUSTRY RECOMMENDATIONS
# ===============================

st.subheader("🏭 Best Industries to Invest")

industries = get_recommendations(selected_country)

for i in industries:
    st.write("•", i)

# ===============================
# SCENARIO SIMULATION
# ===============================

st.subheader("🔮 Scenario Simulation")

inflation_change = st.slider(
    "Simulate Inflation Change (%)",
    -10,
    10,
    0
)

gdp_growth = st.slider(
    "Simulate GDP Growth (%)",
    -10,
    10,
    0
)

simulated_score = country_data.get("Investment Score",0)

simulated_score += gdp_growth * 0.02
simulated_score -= inflation_change * 0.01

st.metric(
    "Simulated Investment Score",
    round(simulated_score,2)
)

# ===============================
# AI BUSINESS INSIGHTS
# ===============================

st.subheader("🧠 AI Business Insights")

insights = []

# Inflation insight
if "Inflation" in df.columns:
    if country_data.get("Inflation", 0) > df["Inflation"].median():
        insights.append("Higher inflation than global median may reduce investment attractiveness.")

# GDP insight
if "GDP" in df.columns:
    if country_data.get("GDP", 0) > df["GDP"].median():
        insights.append("Strong GDP suggests a large and stable economy.")

# Population insight
if "Population" in df.columns:
    if country_data.get("Population", 0) > df["Population"].median():
        insights.append("Large population indicates strong consumer demand.")

# Scenario insight
if simulated_score > country_data.get("Investment Score", 0):
    insights.append("Simulated economic changes improve the investment outlook.")

# Display insights
if insights:
    for i in insights:
        st.write("•", i)
else:
    st.info("No strong insights detected from the current dataset.")

# ===============================
# PDF REPORT GENERATION
# ===============================

st.subheader("📄 Generate Investment Report")

if st.button("Generate PDF Report"):

    report_data = {
        "Country": selected_country,
        "GDP": country_data.get("GDP"),
        "Inflation": country_data.get("Inflation"),
        "Population": country_data.get("Population"),
        "Investment Score": country_data.get("Investment Score"),
        "Industries": industries
    }

    pdf_file = generate_pdf_report(report_data)

    with open(pdf_file, "rb") as f:
        st.download_button(
            "Download PDF",
            data=f,
            file_name="investment_report.pdf",
            mime="application/pdf"
        )
