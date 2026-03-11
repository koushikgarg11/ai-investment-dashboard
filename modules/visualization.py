import plotly.express as px

def country_comparison(df, countries, metric="Investment Score"):
    df_selected = df[df["Country"].isin(countries)]
    fig = px.bar(df_selected, x="Country", y=metric, color=metric,
                 title=f"{metric} Comparison")
    return fig

def investment_heatmap(df):
    fig = px.choropleth(df, locations="Country",
                        locationmode="country names",
                        color="Investment Score",
                        color_continuous_scale="Viridis",
                        title="Global Investment Attractiveness Heatmap")
    return fig
