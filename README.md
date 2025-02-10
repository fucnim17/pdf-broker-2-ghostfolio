# PDF Broker Statements to Ghostfolio

This repository automates the extraction of transaction data from PDF broker statements and imports them directly into [Ghostfolio](https://ghostfol.io/).
Currently, a parser for [Sunrise](https://www.sunrise.app/) is implemented, and additional parsers (e.g., for [Flatex.at](https://www.flatex.at/)) will be added in the future.

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
`"authToken"": "eyJh..." `

Store this token somewhere, you will need it later on. For additional information visit [Ghostfolio](https://github.com/ghostfolio/ghostfolio) and scroll down.

## ⚙️ Configuration
Before running the script, **create a `.env` file** in the project root directory:
```bash
nano .env
```
Then, add the following content (adjust the values to your setup):
```
# 📂 Directory where PDFs are stored
PDF_DIRECTORY=/path/to/your/pdf_folder/
PDF_FILENAME=pdf_name.pdf

# 🌐 Ghostfolio API Settings
GHOSTFOLIO_HOST=http://localhost:3333
GHOSTFOLIO_API_TOKEN=eyJh...
ACCOUNT_ID=your_ghostfolio_account_id
```

## ▶️ Running the Script
To manually run the script:
```bash
python parser/sunrise_parser.py
```

After successful import, the processed PDF will be deleted automatically.

## ⏹️ Deactivating the Virtual Environment
To exit the virtual environment, run: 
```bash
deactivate
```

## 🚀 Planned Features
- **Support for multiple brokers:** More parsers will be added for different statement formats.
- **Automated file monitoring:** The script will run continuously, waiting for new PDFs to process.
- **Improved error handling:** Enhancements for handling edge cases and failed imports.

## 📝 License
This script is licensed under the GNU General Public License Version 3. See the `LICENSE` file for details.


