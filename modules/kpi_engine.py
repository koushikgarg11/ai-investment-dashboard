import numpy as np
import pandas as pd


def calculate_investment_score(df):

    score = 0

    if "GDP" in df.columns:
        score += 0.4 * (df["GDP"] / df["GDP"].max())

    if "Inflation" in df.columns:
        score += 0.3 * (1 / (df["Inflation"] + 1))

    if "Population" in df.columns:
        score += 0.3 * (df["Population"] / df["Population"].max())

    df["Investment Score"] = score

    return df


# ✅ ADD THIS FUNCTION
def top_industries(country):

    industry_map = {
        "India": ["IT Services", "Renewable Energy", "Pharmaceuticals"],
        "Vietnam": ["Electronics Manufacturing", "Textiles", "Semiconductors"],
        "Mexico": ["Automobile Manufacturing", "Electronics", "Logistics"],
        "Brazil": ["Agriculture", "Mining", "Energy"],
        "Indonesia": ["Nickel Mining", "Palm Oil", "Manufacturing"]
    }

    return industry_map.get(country, ["Technology", "Infrastructure", "Energy"])
