import pdfplumber

def extract_text_from_pdf(pdf_path):
    """Extracts and prints text from each page of a given PDF file."""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            print(f"Page {page_num + 1}:\n{text}\n{'-'*40}")

# Test the function with a sample PDF
extract_text_from_pdf("/srv/dev-disk-by-uuid-1662b18d-6525-436b-9831-0d970568c184/data/999_Abrechnungen/Fondsabrechnung (4).pdf")
