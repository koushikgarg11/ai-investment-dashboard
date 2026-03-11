import numpy as np

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
