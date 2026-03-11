from modules.kpi_engine import top_industries


def get_recommendations(country):

    industries = top_industries(country)

    return industries
