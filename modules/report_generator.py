from fpdf import FPDF


def generate_pdf_report(report_data):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Global Investment Intelligence Report", ln=True)

    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, f"Country: {report_data.get('Country','N/A')}", ln=True)
    pdf.cell(0, 10, f"GDP: {report_data.get('GDP','N/A')}", ln=True)
    pdf.cell(0, 10, f"Inflation: {report_data.get('Inflation','N/A')}", ln=True)
    pdf.cell(0, 10, f"Population: {report_data.get('Population','N/A')}", ln=True)
    pdf.cell(0, 10, f"Investment Score: {report_data.get('Investment Score','N/A')}", ln=True)

    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Recommended Industries", ln=True)

    pdf.set_font("Arial", size=12)

    industries = report_data.get("Industries", [])

    for ind in industries:
        pdf.cell(0, 10, f"- {ind}", ln=True)

    file_name = "investment_report.pdf"
    pdf.output(file_name)

    return file_name
