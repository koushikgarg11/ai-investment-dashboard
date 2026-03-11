import streamlit as st
from modules.data_loader import load_macro_data
from modules.kpi_engine import calculate_investment_score
from modules.visualization import country_comparison, investment_heatmap
from modules.scenario import simulate_scenario
from modules.recommendation import get_recommendations
from modules.report_generator import generate_pdf_report
from modules.live_feed import get_live_data

st.set_page_config(page_title="AI Global Investment Dashboard", layout="wide")
st.title("🌎 AI Global Investment Intelligence Platform")

# -----------------------------
# Load macro data
# -----------------------------
df = load_macro_data()
df = calculate_investment_score(df)

# -----------------------------
# Executive Summary Dashboard
# -----------------------------
st.subheader("📊 Executive Summary Dashboard")
selected_country = st.selectbox("Select Country", df["Country"].tolist())
country_data = df[df["Country"]==selected_country].iloc[0]

st.metric("Investment Score", round(country_data["Investment Score"], 2))
st.metric("GDP Growth", country_data["GDP"])
st.metric("Inflation (%)", country_data["Inflation"])
st.metric("FDI (USD Billion)", country_data["FDI"])
st.metric("Unemployment (%)", country_data["Unemployment"])

# -----------------------------
# Live Market Feed
# -----------------------------
st.subheader("💹 Live Market Indicators")
live_data = get_live_data()
for k, v in live_data.items():
    st.metric(k, v)

# -----------------------------
# Country Comparison
# -----------------------------
st.subheader("🌐 Country Comparison")
countries_to_compare = st.multiselect("Select Countries", df["Country"].tolist(),
                                      default=[selected_country])
comparison_chart = country_comparison(df, countries_to_compare)
st.plotly_chart(comparison_chart, use_container_width=True)

# -----------------------------
# Industry Recommendations
# -----------------------------
st.subheader("🏭 Top Industry Recommendations")
industries = get_recommendations(selected_country)
for i, industry in enumerate(industries, 1):
    st.write(f"{i}. {industry}")

# -----------------------------
# Global Heatmap
# -----------------------------
st.subheader("🌍 Global Investment Heatmap")
heatmap_fig = investment_heatmap(df)
st.plotly_chart(heatmap_fig, use_container_width=True)

# -----------------------------
# Scenario Simulation
# -----------------------------
st.subheader("⚡ Scenario Simulation")
st.write("Simulate changes in GDP, Inflation, FDI, and Unemployment")
gdp_change = st.number_input("GDP Change", value=0.0)
inflation_change = st.number_input("Inflation Change", value=0.0)
fdi_change = st.number_input("FDI Change", value=0.0)
unemployment_change = st.number_input("Unemployment Change", value=0.0)

scenario_score = None
if st.button("Simulate Scenario"):
    df_sim = simulate_scenario(df, selected_country, gdp_change, inflation_change, fdi_change, unemployment_change)
    df_sim = calculate_investment_score(df_sim)
    scenario_score = df_sim[df_sim["Country"]==selected_country]["Investment Score"].values[0]
    st.success(f"New Investment Score for {selected_country}: {round(scenario_score,2)}")

# -----------------------------
# Generate PDF Report
# -----------------------------
st.subheader("📄 Download AI Report")
if st.button("Generate PDF Report"):
    pdf_file = generate_pdf_report(country_data, industries, scenario_score)
    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📥 Download PDF",
            data=f,
            file_name=pdf_file,
            mime="application/pdf"
        )
