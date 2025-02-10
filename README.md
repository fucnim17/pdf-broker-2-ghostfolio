# PDF Broker Statements to Ghostfolio

This repository automates the extraction of transaction data from PDF broker statements and imports them directly into [Ghostfolio](https://ghostfol.io/).
Currently, a parser for [Sunrise](https://www.sunrise.app/) is implemented, and additional parsers (e.g., for [flatex.at](https://www.flatex.at/)) will be added in the future.

## 🚀 Planned Features
- Support for multiple brokers (e.g., [flatex.at](https://www.flatex.at/)).
- Automatic PDF folder monitoring: The script will **watch a directory** and process new files as they appear.

## 🛠️ Installation
Clone the repository and set up a virtual environment:
```bash
git clone https://github.com/fucnim17/pdf-broker-2-ghostfolio.git
cd pdf-broker-2-ghostfolio
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🔑 Getting a Ghostfolio Access Token
To import transactions, you need an Bearer Token from Ghostfolio. In order to get one, past the following text in your console (at <INSERT_SECURITY_TOKEN_OF_ACCOUNT>, you have to insert your Security From your GHostfolio Account):
```bash
curl -X POST http://localhost:3333/api/v1/auth/anonymous \
     -H "Content-Type: application/json" \
     -d '{ "accessToken": "<INSERT_SECURITY_TOKEN_OF_ACCOUNT>" }'
```

You will get your access token as a response like this:
`"accessToken": "eyJh..." `

Store this token somewhere, you will need it later on.

For additional information visit [Ghostfolio](https://ghostfol.io/) and scroll down.

## ⚙️ Configuration
Before running the script, configure the following settings in `parser/sunrise_parser.py`:

     1. PDF dawd



## ▶️ Running the Script
To manually run the script:

`python parser/sunrise_parser.py`

After successful import, the processed PDF will be deleted automatically.

## ⏹️ Deactivating the Virtual Environment
To exit the virtual environment, run:
