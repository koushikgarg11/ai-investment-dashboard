import plotly.express as px


def investment_heatmap(df):

    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Investment Score",
        color_continuous_scale="Greens",
        title="Global Investment Attractiveness"
    )

    return fig


def country_comparison(df, countries):

    filtered = df[df["Country"].isin(countries)]

    fig = px.bar(
        filtered,
        x="Country",
        y="Investment Score",
        color="Country",
        title="Country Investment Comparison"
    )

    return fig
