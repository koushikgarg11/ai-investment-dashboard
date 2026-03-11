def simulate_scenario(df, country, gdp_change=0, inflation_change=0, fdi_change=0, unemployment_change=0):
    """
    Adjust macro values for scenario simulation
    """
    df_sim = df.copy()
    idx = df_sim[df_sim["Country"]==country].index[0]

    df_sim.at[idx, "GDP"] += gdp_change
    df_sim.at[idx, "Inflation"] += inflation_change
    df_sim.at[idx, "FDI"] += fdi_change
    df_sim.at[idx, "Unemployment"] += unemployment_change

    return df_sim
