import pdfplumber

def extract_text_from_pdf(pdf_path):
    """Extracts and prints text from each page of a given PDF file."""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            print(f"Page {page_num + 1}:\n{text}\n{'-'*40}")

# Test the function with a sample PDF
extract_text_from_pdf("beispiel.pdf")
