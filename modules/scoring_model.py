import numpy as np

def calculate_score(df):

    df["Investment Score"] = (
        0.35*(df["GDP"]/df["GDP"].max()) +
        0.25*(1/(df["Inflation"])) +
        0.20*(df["Population"]/df["Population"].max()) +
        0.20*(df["FDI"]/df["FDI"].max())
    )

    df["Investment Score"] = df["Investment Score"]*100

    return df
