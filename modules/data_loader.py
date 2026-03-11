import pandas as pd
import streamlit as st

@st.cache_data(ttl=60*60*24*180)  # cache for 6 months
def load_macro_data(file_path="datasets/macro_data.csv"):
    """
    Load macroeconomic data for all countries.
    Columns example: Country,GDP,Inflation,FDI,Unemployment
    """
    df = pd.read_csv(file_path)
    return df
  
