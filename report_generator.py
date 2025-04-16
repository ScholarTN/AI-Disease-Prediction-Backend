from fpdf import FPDF
from datetime import datetime

def generate_pdf(records):
    pdf = FPDF()
    
    # Add a cover page if there are multiple records
    if len(records) > 1:
        pdf.add_page()
        pdf.set_font("Arial", size=16, style='B')
        pdf.cell(200, 10, txt="Diabetes Prediction Reports", ln=True, align="C")
        pdf.ln(20)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Total Records: {len(records)}", ln=True)
        pdf.ln(30)
    
    for record in records:
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Remove unwanted fields
        record_data = {k: v for k, v in record.items() 
                     if k not in ['_id', 'processed_input']}
        
        # Header
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(200, 10, txt="Diabetes Prediction Report", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        
        # Format timestamp
        if 'timestamp' in record_data:
            if isinstance(record_data['timestamp'], datetime):
                record_data['timestamp'] = record_data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            elif record_data['timestamp'] is None:
                record_data['timestamp'] = "Unknown date"
        
        # Add data
        for key, value in record_data.items():
            if key == 'prediction':
                risk = "High Risk" if value == 1 else "Low Risk"
                pdf.set_text_color(255, 0, 0) if value == 1 else pdf.set_text_color(0, 128, 0)
                pdf.set_font("Arial", size=12, style='B')
                pdf.cell(200, 10, txt=f"Risk Assessment: {risk}", ln=True)
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("Arial", size=12)
            else:
                formatted_key = key.replace('_', ' ').title()
                pdf.cell(90, 10, txt=f"{formatted_key}:", ln=0)
                pdf.cell(100, 10, txt=str(value), ln=True)
        
        pdf.ln(10)
    
    # Return PDF as bytes (modified to ensure proper encoding)
    try:
        pdf_output = pdf.output(dest='S')
        if isinstance(pdf_output, str):
            return pdf_output.encode('latin-1')
        return bytes(pdf_output)
    except Exception as e:
        raise ValueError(f"PDF generation failed: {str(e)}")
