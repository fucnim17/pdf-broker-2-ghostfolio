import pdfplumber
import re
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Define directories
PDF_DIRECTORY = os.getenv("PDF_DIRECTORY")
PDF_FILE = PDF_DIRECTORY + os.getenv("PDF_FILENAME")

# Define Ghostfolio API settings
GHOSTFOLIO_HOST = os.getenv("GHOSTFOLIO_HOST")
API_TOKEN = os.getenv("API_TOKEN")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

def parse_sunrise_pdf(pdf_path):
    """Extracts transaction details from a PDF file and prepares JSON for Ghostfolio API."""
    transactions = []

    # Open and extract text from all pages
    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

    # Regex pattern for detecting transactions with line breaks
    pattern = re.compile(
        r"(Kauf|Verkauf)\s+Standortfonds\s+[A-Za-zäöüÄÖÜß]*\s*([\d.,]+)\s*€\s+([\d.,]+)\s*€\s+([\d.,]+)\s*\n"
        r"([A-Z0-9]{12})\s+(\d{2}\.\d{2}\.\d{4})"
    )

    matches = pattern.findall(full_text)

    # Process each detected transaction
    for match in matches:
        action = "BUY" if match[0] == "Kauf" else "SELL"
        price = float(match[2].replace(",", "."))  # Convert price to float
        quantity = float(match[3].replace(",", "."))  # Convert quantity to float
        isin = match[4]  # Extract ISIN
        date_iso = convert_date_format(match[5])  # Convert date to ISO-8601 format

        transactions.append({
            "currency": "EUR",
            "dataSource": "YAHOO",
            "date": date_iso,
            "fee": 0.00,
            "quantity": quantity,
            "symbol": isin,
            "type": action,
            "unitPrice": price,
            "accountId": ACCOUNT_ID,
            "comment": "imported with https://github.com/fucnim17/pdf-broker-2-ghostfolio.git"
        })

    # If no transactions were found, print a warning
    if not transactions:
        print("❌ No transactions found. Check the regex pattern or extracted text.")

    return {"activities": transactions}

def convert_date_format(date_str):
    """Converts date from DD.MM.YYYY to ISO-8601 format for Ghostfolio."""
    day, month, year = date_str.split(".")
    return f"{year}-{month}-{day}T00:00:00.000Z"

def upload_to_ghostfolio(json_data):
    """Uploads JSON transaction data to Ghostfolio API."""
    url = f"{GHOSTFOLIO_HOST}/api/v1/import"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=json_data)

    # Handle response
    if response.status_code == 201:
        print("✅ Successfully imported into Ghostfolio!")
        return True
    else:
        print(f"❌ Import failed: {response.status_code}")
        print(response.text)
        return False

def delete_pdf_if_success(pdf_path, success):
    """Deletes the PDF file if the import was successful."""
    if success:
        try:
            os.remove(pdf_path)
            print(f"🗑️ Successfully deleted {pdf_path}")
        except Exception as e:
            print(f"⚠️ Could not delete {pdf_path}: {e}")

# Parse PDF and generate JSON data for Ghostfolio
json_data = parse_sunrise_pdf(PDF_FILE)

# Send data to Ghostfolio
success = upload_to_ghostfolio(json_data)

# Delete PDF if import was successful
delete_pdf_if_success(PDF_FILE, success)
