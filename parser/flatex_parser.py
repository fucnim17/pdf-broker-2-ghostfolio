import pdfplumber
import re
import csv
import requests
from datetime import datetime

# Exchange Rates API (historische Wechselkurse von der EZB)
EXCHANGE_RATE_API = "https://api.exchangeratesapi.io"
API_KEY = "805b8dc40c8de2a251859b43bc0490db"

# Define fixed directories
PDF_DIRECTORY = "/root/pdf-broker-2-ghostfolio/"
CSV_DIRECTORY = "/root/pdf-broker-2-ghostfolio/"
SECURITIES_FILE = "/root/pdf-broker-2-ghostfolio/securities.csv"

# Define file names
PDF_FILE = PDF_DIRECTORY + "beispiel.pdf"
CSV_FILE = CSV_DIRECTORY + "output.csv"

def get_security_currency(isin):
    """Reads securities.csv to get the base currency of a security."""
    with open(SECURITIES_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["ISIN"] == isin:
                return row["BaseCurrency"]
    return "EUR"  # Default to EUR if not found

def get_exchange_rate(date, security_currency):
    """Fetches the exchange rate from EUR to the security's base currency."""
    
    if security_currency == "EUR":
        return 1.0  # Kein Wechselkurs nötig, wenn das Wertpapier in EUR notiert

    url = f"{EXCHANGE_RATE_API}/{date}?access_key={API_KEY}&base=EUR&symbols={security_currency}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if "rates" in data and security_currency in data["rates"]:
            print(f"Exchange rate for {date} EUR/{security_currency}: {data['rates'][security_currency]}")
            return data["rates"][security_currency]
        else:
            print(f"No exact match for {date}, fetching latest available rate.")
            latest_url = f"{EXCHANGE_RATE_API}/latest?access_key={API_KEY}&base=EUR&symbols={security_currency}"
            response = requests.get(latest_url)
            latest_data = response.json()

            if "rates" in latest_data and security_currency in latest_data["rates"]:
                print(f"Using latest available rate: {latest_data['rates'][security_currency]}")
                return latest_data["rates"][security_currency]

            return 1.0  # Fallback if no data at all
    except Exception as e:
        print(f"API request failed: {e}")
        return 1.0  # Fallback if API fails


def parse_flatex_pdf(pdf_path):
    """Parses a flatex PDF file and extracts transaction details."""
    transactions = []

    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

    # Extract transaction date
    match = re.search(r"Handelstag (\d{2}\.\d{2}\.\d{4})", full_text)
    date = datetime.strptime(match.group(1), "%d.%m.%Y").strftime("%Y-%m-%d") if match else ""

    # Extract security name and ISIN
    match = re.search(r"Kauf (.*?) \((\w{12})", full_text)
    asset = match.group(1).strip() if match else ""
    isin = match.group(2).strip() if match else ""

    # Extract quantity
    match = re.search(r"Ausgeführt\s*:\s*([\d,]+)\s*St\.", full_text)
    quantity = float(match.group(1).replace(",", ".")) if match else 0.0

    # Extract price per unit
    match = re.search(r"Kurs\s*:\s*([\d,]+)\s*EUR", full_text)
    price_eur = float(match.group(1).replace(",", ".")) if match else 0.0

    # Extract total amount (negative for buy, positive for sell)
    match = re.search(r"Endbetrag\s*:\s*([-]?\d+,\d+)\s*EUR", full_text)
    total_amount_eur = float(match.group(1).replace(",", ".")) if match else 0.0

    # Get the base currency of the asset
    base_currency = get_security_currency(isin)

    # Convert amount if necessary
    price = price_eur
    total_amount = total_amount_eur
    if base_currency != "EUR":
    	exchange_rate = get_exchange_rate(date, base_currency)
    	price = round(price_eur * exchange_rate, 6)
    	total_amount = round(total_amount_eur * exchange_rate, 2)

    # Define action type (buy/sell)
    action = "buy" if total_amount < 0 else "sell"

    # Construct transaction dictionary
    transactions.append({
        "Date": date,
        "Code": isin if isin else asset,
        "DataSource": "YAHOO",
        "Currency": base_currency,
        "Price": f"{price:.6f}",
        "Quantity": f"{quantity:.6f}",
        "Action": action,
        "Fee": "0.00",
        "Note": ""
    })

    return transactions

def export_to_csv(transactions, output_path):
    """Exports transactions to CSV in the required format."""
    fieldnames = ["Date", "Code", "DataSource", "Currency", "Price", "Quantity", "Action", "Fee", "Note"]

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in transactions:
            writer.writerow(row)

    print(f"CSV saved to {output_path}")

# Run the script with the fixed file paths
transactions = parse_flatex_pdf(PDF_FILE)
export_to_csv(transactions, CSV_FILE)
