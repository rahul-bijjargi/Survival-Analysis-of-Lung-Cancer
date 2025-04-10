import pdfplumber

def extract_text_from_pdf(pdf_file):
    try:
        text = ''
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + '\n'
        return text
    except Exception as e:
        print(" Error in extract_text_from_pdf:", e)
        return ""

def parse_cancer_report(text):
    data = {}
    lines = text.split('\n')
    for line in lines:
        if '.' in line:
            try:
                key, value = line.split('.', 1)
                key = key.strip()
                value = value.strip()
                if value.isdigit():
                    data[key] = int(value)
            except Exception as e:
                # Log error for the specific line if needed:
                print(f"Error parsing line: {line} → {e}")
                continue
    return data
