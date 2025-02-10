# PDF Broker Statements to Ghostfolio

This repository automates the extraction of transaction data from PDF broker statements and imports them directly into [Ghostfolio](https://ghostfol.io/).
Currently, a parser for **Sunrise Securities** is implemented, and additional parsers (e.g., for **Flatex Austria**) will be added in the future.

## 🚀 Planned Features
- Support for multiple brokers (e.g., **Flatex Austria**).
- Automatic PDF folder monitoring: The script will **watch a directory** and process new files as they appear.
- Fully automated import into **Ghostfolio**.

## 🛠️ Installation
Clone the repository and set up a virtual environment:
```bash
git clone https://github.com/fucnim17/pdf-broker-2-ghostfolio.git
cd pdf-broker-2-ghostfolio
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ▶️ unning the Script
To manually run the script:

`python parser/sunrise_parser.py`

After successful import, the processed PDF will be deleted automatically.

## ⏹️ Deactivating the Virtual Environment
To exit the virtual environment, run:
