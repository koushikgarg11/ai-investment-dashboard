import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from fpdf import FPDF

st.set_page_config(page_title="AI Global Investment Intelligence Platform", layout="wide")

st.title("🌍 AI Global Investment Intelligence Platform")

st.write("Analyze investment attractiveness across all countries using macroeconomic indicators.")

# =========================
# LOAD GLOBAL DATA
# =========================

@st.cache_data
def load_data():

    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

    df = pd.read_csv(url)

    df = df[["country","population","gdp"]]

    df = df.dropna()

    df = df.rename(columns={
        "country":"Country",
        "population":"Population",
        "gdp":"GDP"
    })

    df = df.groupby("Country").last().reset_index()

    # Simulated inflation (because dataset doesn't include it)
    df["Inflation"] = 2 + (df["GDP"] % 8)

    return df


df = load_data()

# =========================
# INVESTMENT SCORE MODEL
# =========================

def calculate_score(df):

    df["Investment Score"] = (
        0.4*(df["GDP"]/df["GDP"].max()) +
        0.3*(df["Population"]/df["Population"].max()) +
        0.3*(1/(df["Inflation"]+1))
    )

    df["Investment Score"] = df["Investment Score"]*100

    return df


df = calculate_score(df)

# =========================
# SIDEBAR CONTROLS
# =========================

countries = sorted(df["Country"].unique())

selected_country = st.sidebar.selectbox("Select Country", countries)

compare = st.sidebar.multiselect("Compare Countries", countries, default=[selected_country])

# =========================
# EXECUTIVE DASHBOARD
# =========================

st.subheader("📊 Executive Summary")

country_data = df[df["Country"] == selected_country].iloc[0]

col1,col2,col3,col4 = st.columns(4)

col1.metric("GDP", f"${country_data['GDP']:,.0f}")
col2.metric("Population", f"{country_data['Population']:,.0f}")
col3.metric("Inflation", round(country_data["Inflation"],2))
col4.metric("Investment Score", round(country_data["Investment Score"],2))

# =========================
# GLOBAL HEATMAP
# =========================

st.subheader("🌎 Global Investment Heatmap")

fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Investment Score",
    color_continuous_scale="Greens",
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# COUNTRY COMPARISON
# =========================

st.subheader("📊 Country Comparison")

compare_df = df[df["Country"].isin(compare)]

fig2 = px.bar(
    compare_df,
    x="Country",
    y="Investment Score",
    color="Country"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# INDUSTRY RECOMMENDATION
# =========================

st.subheader("🏭 Recommended Industries")

industry_map = {

    "India":["IT Services","Renewable Energy","EV Manufacturing"],
    "Vietnam":["Electronics Manufacturing","Textiles","Semiconductors"],
    "Mexico":["Automobile","Electronics","Logistics"],
    "Brazil":["Agriculture","Mining","Energy"]
}

industries = industry_map.get(selected_country, ["Technology","Infrastructure","Energy"])

for i in industries:
    st.write("•", i)

# =========================
# SCENARIO SIMULATION
# =========================

st.subheader("🔮 Scenario Simulation")

inflation_change = st.slider("Inflation Change %", -5,5,0)
gdp_growth = st.slider("GDP Growth %", -5,5,0)

sim_score = country_data["Investment Score"]

sim_score += gdp_growth*2
sim_score -= inflation_change*1.5

st.metric("Simulated Investment Score", round(sim_score,2))

# =========================
# AI BUSINESS INSIGHTS
# =========================

st.subheader("🧠 AI Business Insights")

insights = []

if country_data["GDP"] > df["GDP"].median():
    insights.append("Country has strong economic size.")

if country_data["Population"] > df["Population"].median():
    insights.append("Large consumer market.")

if country_data["Inflation"] > 6:
    insights.append("High inflation may reduce investment attractiveness.")

if sim_score > country_data["Investment Score"]:
    insights.append("Economic scenario improves investment outlook.")

if insights:
    for i in insights:
        st.write("•", i)
else:
    st.info("No major insights detected.")

# =========================
# PDF REPORT
# =========================

st.subheader("📄 Investment Report")

if st.button("Generate Report"):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"Investment Report",ln=True)

    pdf.set_font("Arial","",12)

    pdf.cell(0,10,f"Country: {selected_country}",ln=True)
    pdf.cell(0,10,f"GDP: {country_data['GDP']}",ln=True)
    pdf.cell(0,10,f"Population: {country_data['Population']}",ln=True)
    pdf.cell(0,10,f"Inflation: {country_data['Inflation']}",ln=True)
    pdf.cell(0,10,f"Investment Score: {country_data['Investment Score']}",ln=True)

    file = "report.pdf"

    pdf.output(file)

    with open(file,"rb") as f:

        st.download_button("Download Report", f, file_name="investment_report.pdf")
