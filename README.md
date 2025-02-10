# PDF Broker Statements to Ghostfolio

This repository automates the extraction of transaction data from PDF broker statements and imports them directly into [Ghostfolio](https://ghostfol.io/).
Currently, a parser for [Sunrise](https://www.sunrise.app/) is implemented, and additional parsers (e.g., for [flatex.at](https://www.flatex.at/)) will be added in the future.

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
To import transactions, you need a Bearer Token from Ghostfolio. To get one, paste the following text into your console, replacing `<INSERT_SECURITY_TOKEN_OF_ACCOUNT>` with the security token from your Ghostfolio account:
```bash
curl -X POST http://localhost:3333/api/v1/auth/anonymous \
     -H "Content-Type: application/json" \
     -d '{ "accessToken": "<INSERT_SECURITY_TOKEN_OF_ACCOUNT>" }'
```

You will get your access token as a response like this:
`"accessToken": "eyJh..." `

Store this token somewhere, you will need it later on. For additional information visit [Ghostfolio](https://github.com/ghostfolio/ghostfolio) and scroll down.

## ⚙️ Configuration
Before running the script, configure the following settings in `parser/sunrise_parser.py`:

1. `PDF_DIRECTORY` is the folder where broker statements are stored
2. `PDF_FILE` is the name of your broker statement
3. `GHOSTFOLIO_HOST` is your Ghostfolio instance
4. `API_TOKEN` is your Bearer Token
5. `ACCOUNT_ID` is your ID from one of your Ghostfolio accounts 

## ▶️ Running the Script
To manually run the script:

`python parser/sunrise_parser.py`

After successful import, the processed PDF will be deleted automatically.

## ⏹️ Deactivating the Virtual Environment
To exit the virtual environment, run: `deactivate`

## 🚀 Planned Features
- **Support for multiple brokers:** More parsers will be added for different statement formats.
- **Automated file monitoring:** The script will run continuously, waiting for new PDFs to process.
- **Improved error handling:** Enhancements for handling edge cases and failed imports.

## 📝 License
This script is licensed under the GNU General Public License Version 3. See the `LICENSE` file for details.


