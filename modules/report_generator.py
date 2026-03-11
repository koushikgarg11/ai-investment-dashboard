from fpdf import FPDF


def generate_report(data):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"Global Investment Report",ln=True)

    pdf.ln(10)

    pdf.set_font("Arial","",12)

    for k,v in data.items():

        if isinstance(v,list):

            pdf.cell(0,10,f"{k}:",ln=True)

            for i in v:
                pdf.cell(0,10,f"- {i}",ln=True)

        else:

            pdf.cell(0,10,f"{k}: {v}",ln=True)

    file="investment_report.pdf"
    pdf.output(file)

    return file
