def calculate_investment_score(df):
    """
    Weighted formula for investment attractiveness:
    Score = 0.4*GDP + 0.3*(1/Inflation) + 0.2*FDI + 0.1*(1/Unemployment)
    """
    df = df.copy()
    df["Investment Score"] = (
        0.4*df["GDP"] +
        0.3*(1/df["Inflation"]) +
        0.2*df["FDI"] +
        0.1*(1/df["Unemployment"])
    )
    return df

def top_industries(country_name):
    industry_map = {
        "India": ["IT & Software", "Textiles", "Renewable Energy"],
        "Vietnam": ["Electronics Manufacturing", "Textiles", "Agriculture"],
        "Mexico": ["Automotive", "Tourism", "Manufacturing"]
    }
    return industry_map.get(country_name, ["General Manufacturing", "Services", "Energy"])
