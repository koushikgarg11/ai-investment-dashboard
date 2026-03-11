import streamlit as st
import pandas as pd

from modules.data_loader import load_data
from modules.scoring_model import calculate_score
from modules.visualization import investment_heatmap,country_comparison
from modules.recommendation import recommend_industries
from modules.report_generator import generate_report


st.set_page_config(
    page_title="AI Global Investment Intelligence Platform",
    layout="wide"
)

st.title("🌍 AI Global Investment Intelligence Platform")

st.write(
"Analyze global investment opportunities using macroeconomic indicators."
)

# Load data
df = load_data()

df = calculate_score(df)

# Sidebar
st.sidebar.header("Controls")

countries = df["Country"].tolist()

selected_country = st.sidebar.selectbox(
    "Select Country",
    countries
)

compare = st.sidebar.multiselect(
    "Compare Countries",
    countries,
    default=[selected_country]
)

# Executive dashboard
st.subheader("📊 Executive Summary")

country_data = df[df["Country"]==selected_country].iloc[0]

col1,col2,col3,col4 = st.columns(4)

col1.metric("GDP",round(country_data["GDP"],2))
col2.metric("Inflation",round(country_data["Inflation"],2))
col3.metric("Population",round(country_data["Population"],2))
col4.metric("Investment Score",round(country_data["Investment Score"],2))

# Global map
st.subheader("🌎 Global Investment Heatmap")

heatmap = investment_heatmap(df)

st.plotly_chart(heatmap,use_container_width=True)

# Country comparison
st.subheader("📊 Country Comparison")

chart = country_comparison(df,compare)

st.plotly_chart(chart,use_container_width=True)

# Industry recommendation
st.subheader("🏭 Best Industries to Invest")

industries = recommend_industries(selected_country)

for i in industries:
    st.write("•",i)

# Scenario simulation
st.subheader("🔮 Scenario Simulation")

inflation_change = st.slider(
    "Inflation Change %",
    -5,5,0
)

gdp_growth = st.slider(
    "GDP Growth %",
    -5,5,0
)

new_score = country_data["Investment Score"]

new_score += gdp_growth*2
new_score -= inflation_change*1.5

st.metric("Simulated Investment Score",round(new_score,2))

# Generate report
st.subheader("📄 Investment Report")

if st.button("Generate PDF Report"):

    report_data = {
        "Country":selected_country,
        "GDP":country_data["GDP"],
        "Inflation":country_data["Inflation"],
        "Population":country_data["Population"],
        "Investment Score":country_data["Investment Score"],
        "Recommended Industries":industries
    }

    file = generate_report(report_data)

    with open(file,"rb") as f:

        st.download_button(
            "Download Report",
            f,
            file_name="investment_report.pdf"
        )
