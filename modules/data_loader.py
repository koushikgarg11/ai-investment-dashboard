import pandas as pd
import requests
import streamlit as st

@st.cache_data
def load_macro_data():

    url = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json&per_page=20000"

    response = requests.get(url)
    data = response.json()[1]

    records = []

    for item in data:
        if item["value"] is not None:
            records.append({
                "Country": item["country"]["value"],
                "Year": item["date"],
                "GDP": item["value"]
            })

    df = pd.DataFrame(records)

    return df
