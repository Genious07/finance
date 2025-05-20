# AI Powered Stock Analyzer

An AI-driven Streamlit application that fetches and analyzes stock data using Yahoo Finance, scrapes basic web snippets, and generates comprehensive investment reports via the Groq LLM API.

## 🔗 Repository

[https://github.com/Genious07/finance.git](https://github.com/Genious07/finance.git)

## 🚀 Features

* **Real-time Stock Data**: Fetches company info, key metrics, and 1-year price history via [yfinance](https://pypi.org/project/yfinance/).
* **Financial Summaries**: Parses and displays quarterly income statements, balance sheets, and cash flow summaries.
* **Major Holders & Analyst Recommendations**: Retrieves top institutional holders and latest analyst ratings.
* **Simulated Web Search**: Demonstrates basic scraping of top news snippets (with placeholder logic).
* **AI-Powered Reports**: Generates in-depth markdown reports using the Groq API and Llama 3 model.
* **Interactive UI**: Built with [Streamlit](https://streamlit.io/) for responsive, tabbed displays and charts.
* **Extensible**: Designed to add custom search APIs or additional data sources in future enhancements.

## 🛠️ Tech Stack

| Component            | Library / Service        |
| -------------------- | ------------------------ |
| Web Framework        | Streamlit                |
| Financial Data       | yfinance                 |
| Web Scraping         | requests, BeautifulSoup  |
| LLM Integration      | Groq API (Llama 3 model) |
| Data Handling        | pandas, json             |
| Environment & Config | os (env vars)            |

## 📋 Prerequisites

* Python 3.8+ installed on your system.
* A valid Groq API key. Sign up at [https://console.groq.com/keys](https://console.groq.com/keys) and set the `GROQ_API_KEY` environment variable.

## 🔧 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Genious07/finance.git
   cd finance
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   venv\Scripts\activate.bat     # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. Obtain your Groq API key from [https://console.groq.com/keys](https://console.groq.com/keys).
2. Export the key as an environment variable:

   ```bash
   export GROQ_API_KEY="your_api_key_here"   # macOS/Linux
   set GROQ_API_KEY="your_api_key_here"      # Windows (CMD)
   ```

## 🏃‍♂️ Running the App

Launch the Streamlit application:

```bash
streamlit run main.py
```

* Open the provided local URL (usually [http://localhost:8501](http://localhost:8501)).
* Enter a valid stock ticker symbol (e.g., `AAPL`, `MSFT`, `RELIANCE.NS`, `BHP.AX`) in the sidebar.
* Click **Analyze Stock** to fetch data and generate the interactive report.

## 📂 Project Structure

```plaintext
finance/
├── main.py              # Streamlit app entrypoint
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation (you are here)
└── .gitignore           # Ignored files and folders
```

## 📝 Usage Overview

1. **Company Info & Summary**: View core metrics, business summary, sector, and industry.
2. **Price History**: Inspect a 1-year closing-price chart and recent data table.
3. **Financials & Holders**: Read quarterly financial snapshots and see major institutional holders and analyst recommendations.
4. **Web Search (Simulated)**: Preview placeholder news snippets with links for manual inspection.
5. **AI Generated Report**: Receive a structured markdown report covering:

   * Company overview
   * Financial analysis
   * Market sentiment & news
   * Risk assessment
   * Opportunities & growth drivers
   * Balanced investment outlook summary

## 🔍 Extending & Customizing

* **Search API**: Replace the simulated `search_web_for_stock` logic with a real search API (e.g., Google Custom Search JSON API).
* **Data Sources**: Integrate additional data feeds (e.g., Alpha Vantage, IEX Cloud).
* **Model Choices**: Swap Llama models or configure alternative LLM providers.

## 📜 License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

## ⚠️ Disclaimer

All financial data and AI-generated content are for informational purposes only and do not constitute financial advice. Always conduct your own research or consult a professional before making investment decisions.

---

*Built with ❤️ by Genious07*
