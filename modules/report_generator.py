from fpdf import FPDF

def generate_pdf_report(country_data, industries, scenario_score=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"AI Investment Report: {country_data['Country']}", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.ln(5)
    pdf.cell(0, 8, f"Investment Score: {round(country_data['Investment Score'],2)}", ln=True)
    pdf.cell(0, 8, f"GDP Growth: {country_data['GDP']}", ln=True)
    pdf.cell(0, 8, f"Inflation: {country_data['Inflation']}%", ln=True)
    pdf.cell(0, 8, f"FDI: {country_data['FDI']} Billion USD", ln=True)
    pdf.cell(0, 8, f"Unemployment: {country_data['Unemployment']}%", ln=True)

    pdf.ln(5)
    pdf.cell(0, 8, "Top Industries Recommended:", ln=True)
    for i, industry in enumerate(industries, 1):
        pdf.cell(0, 6, f"{i}. {industry}", ln=True)

    if scenario_score is not None:
        pdf.ln(5)
        pdf.cell(0, 8, f"Scenario Simulation Score: {round(scenario_score,2)}", ln=True)

    filename = f"{country_data['Country']}_investment_report.pdf"
    pdf.output(filename)
    return filename
