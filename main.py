import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from groq import Groq
import os
import pandas as pd
import json # For robustly handling yfinance data

# --- Configuration ---
# Ensure your Groq API key is set as an environment variable: GROQ_API_KEY
# You can get a Groq API key from https://console.groq.com/keys
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    GROQ_API_KEY_SET = bool(os.environ.get("GROQ_API_KEY"))
except Exception as e:
    st.error(f"Error initializing Groq client: {e}. Is GROQ_API_KEY set?")
    GROQ_API_KEY_SET = False
    client = None

# --- Helper Functions ---

def fetch_stock_data(ticker_symbol):
    """
    Fetches stock data from Yahoo Finance.
    Returns a dictionary with various stock details or None if an error occurs.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        
        # Fetch various pieces of information
        info = stock.info
        
        # Convert non-serializable parts of info to string or handle them
        # For example, 'companyOfficers' might be a list of dicts
        # This is a basic sanitization; more complex structures might need specific handling
        for key, value in info.items():
            if isinstance(value, list) and value and isinstance(value[0], dict):
                try:
                    json.dumps(value) # Test if serializable
                except TypeError:
                    info[key] = str(value) # Convert to string if not
            elif not isinstance(value, (str, int, float, bool, type(None))):
                 # Attempt to convert other complex types to string
                try:
                    json.dumps({key: value})
                except TypeError:
                    info[key] = str(value)


        hist_1y = stock.history(period="1y")
        
        major_holders = None
        try:
            major_holders_df = stock.major_holders
            if major_holders_df is not None and not major_holders_df.empty:
                major_holders = major_holders_df.to_string()
        except Exception as e:
            st.warning(f"Could not fetch major holders for {ticker_symbol}: {e}")
            major_holders = "Not available or error fetching."

        recommendations = None
        try:
            recommendations_df = stock.recommendations
            if recommendations_df is not None and not recommendations_df.empty:
                recommendations = recommendations_df.tail().to_string() # Last 5 recommendations
            else:
                recommendations = "No recommendations data available."
        except Exception as e:
            st.warning(f"Could not fetch recommendations for {ticker_symbol}: {e}")
            recommendations = "Not available or error fetching."

        financials_summary = {}
        try:
            financials_summary['income_statement_quarterly'] = stock.quarterly_income_stmt.iloc[:, :2].to_string() if stock.quarterly_income_stmt is not None and not stock.quarterly_income_stmt.empty else "Not available"
            financials_summary['balance_sheet_quarterly'] = stock.quarterly_balance_sheet.iloc[:, :2].to_string() if stock.quarterly_balance_sheet is not None and not stock.quarterly_balance_sheet.empty else "Not available"
            financials_summary['cash_flow_quarterly'] = stock.quarterly_cashflow.iloc[:, :2].to_string() if stock.quarterly_cashflow is not None and not stock.quarterly_cashflow.empty else "Not available"
        except Exception as e:
            st.warning(f"Could not fetch some financial statements for {ticker_symbol}: {e}")
            if 'income_statement_quarterly' not in financials_summary: financials_summary['income_statement_quarterly'] = "Error fetching."
            if 'balance_sheet_quarterly' not in financials_summary: financials_summary['balance_sheet_quarterly'] = "Error fetching."
            if 'cash_flow_quarterly' not in financials_summary: financials_summary['cash_flow_quarterly'] = "Error fetching."


        # Safely get attributes, providing defaults if they don't exist
        company_name = info.get('longName', ticker_symbol)
        sector = info.get('sector', 'N/A')
        industry = info.get('industry', 'N/A')
        summary = info.get('longBusinessSummary', 'N/A')
        
        # Select a subset of 'info' for brevity in the LLM prompt, if needed
        # For now, we'll pass a good chunk but be mindful of token limits
        relevant_info_keys = [
            'symbol', 'longName', 'sector', 'industry', 'country', 'website',
            'marketCap', 'enterpriseValue', 'trailingPE', 'forwardPE', 
            'dividendYield', 'beta', '52WeekChange', 'shortRatio',
            'currentPrice', 'targetHighPrice', 'targetLowPrice', 'targetMeanPrice',
            'recommendationKey', 'numberOfAnalystOpinions'
        ]
        brief_info = {k: info.get(k, 'N/A') for k in relevant_info_keys}


        return {
            "ticker": ticker_symbol,
            "company_name": company_name,
            "info": brief_info, # Use the curated brief_info
            "full_info_dump_for_display": info, # For display in UI
            "sector": sector,
            "industry": industry,
            "summary": summary,
            "history_1y": hist_1y,
            "major_holders": major_holders,
            "recommendations": recommendations,
            "financials_summary": financials_summary
        }

    except Exception as e:
        st.error(f"Error fetching data for {ticker_symbol} from Yahoo Finance: {e}")
        return None

def search_web_for_stock(stock_name, num_results=3):
    """
    Simulates a web search for stock news and analysis.
    In a real application, you'd use a proper search API (e.g., Google Search API).
    This function uses a placeholder for search and then attempts to scrape.
    """
    st.info(f"Simulating web search for '{stock_name}'... (This is a placeholder and might not yield deep results without a proper search API)")
    search_query = f"latest news and analysis for {stock_name} stock"
    
    # Placeholder for actual search engine results.
    # For a real app, integrate with Google Search API or similar.
    # For this example, we'll try to construct some search URLs.
    # This is highly unreliable and just for demonstration.
    
    # Attempting a simple DuckDuckGo search URL structure (results may vary)
    # A more robust solution would be to use a library that interfaces with search engines
    # or an actual search API. `googlesearch-python` is an option but can be flaky.
    
    urls = []
    try:
        # Using a simple search URL, this is not true scraping of a search engine
        # but rather constructing a search query URL.
        # For actual search results, a more robust method is needed.
        # This is a simplified approach for demonstration.
        
        # Let's try to use a generic search engine query format.
        # This is NOT a reliable way to get search results.
        # A proper solution would use an API like Google Custom Search JSON API.
        
        # Fallback: Construct a Google search URL for manual inspection if needed
        st.markdown(f"You can manually search on Google: [Search for {stock_name}](https://www.google.com/search?q={search_query.replace(' ', '+')})")
        
        # Since direct programmatic search is complex and often blocked without APIs,
        # this part will be very limited. We'll try to fetch from a couple of financial news sites if possible,
        # but this is highly dependent on their structure and anti-scraping measures.
        
        # For demonstration, let's imagine we got some URLs (these are examples)
        # In a real scenario, these would come from a search API.
        example_urls = [
            f"https://finance.yahoo.com/quote/{stock_name.split(' ')[0]}/news", # Assuming stock_name might be like "AAPL"
            # Add more generic financial news sites if needed, but scraping them is hard
        ]
        
        # This part is more illustrative than functional for broad web scraping.
        # I will return a placeholder message.
        st.warning("Web search simulation is very basic. For real insights, integrate a proper search API or use specific financial news APIs.")
        return ["Web search simulation: No reliable URLs fetched automatically for scraping in this basic example. Consider using financial news APIs for robust data."]

    except Exception as e:
        st.error(f"Error during web search simulation for {stock_name}: {e}")
        return [f"Error during web search: {e}"]

    # The following scraping part is illustrative if URLs were successfully obtained.
    # Given the limitations above, it might not execute with meaningful URLs.
    
    content_snippets = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    for url in urls[:num_results]: # Process only top N results
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text - this is generic and needs refinement for specific sites
            paragraphs = soup.find_all('p', limit=3) # Get first 3 paragraphs
            text_content = ' '.join([p.get_text() for p in paragraphs])
            if text_content:
                content_snippets.append(f"Source: {url}\nSnippet: {text_content[:500]}...") # Limit snippet length
            else:
                content_snippets.append(f"Source: {url}\nSnippet: Could not extract meaningful content.")
        except requests.exceptions.RequestException as e:
            content_snippets.append(f"Source: {url}\nSnippet: Error fetching or parsing URL: {e}")
        except Exception as e:
            content_snippets.append(f"Source: {url}\nSnippet: An unexpected error occurred: {e}")
            
    if not content_snippets:
        return ["No relevant web content found or extracted."]
        
    return content_snippets


def generate_report_with_llm(stock_data, web_search_results, stock_name, ticker_symbol):
    """
    Generates a financial report using Groq API and Llama model.
    """
    if not GROQ_API_KEY_SET or client is None:
        return "Groq API key not configured. Please set the GROQ_API_KEY environment variable."

    # Prepare the data for the prompt
    # We need to be careful about the length of the data passed to the LLM.
    
    # Summary of stock data
    stock_summary_for_llm = f"""
    Company: {stock_data['company_name']} ({ticker_symbol})
    Sector: {stock_data['sector']}
    Industry: {stock_data['industry']}
    Business Summary: {stock_data['summary'][:1000]}... 
    
    Key Financial Info (from stock.info):
    {pd.Series(stock_data['info']).to_string()}

    Recent Price Trend (Last 5 days of 1-year history):
    {stock_data['history_1y'].tail().to_string()}

    Major Holders:
    {stock_data['major_holders']}

    Analyst Recommendations (Recent):
    {stock_data['recommendations']}
    
    Quarterly Financials Summary:
    Income Statement (Recent 2 Qtrs):
    {stock_data['financials_summary']['income_statement_quarterly']}
    
    Balance Sheet (Recent 2 Qtrs):
    {stock_data['financials_summary']['balance_sheet_quarterly']}
    
    Cash Flow (Recent 2 Qtrs):
    {stock_data['financials_summary']['cash_flow_quarterly']}
    """

    # Summary of web search results
    web_summary_for_llm = "\n".join([f"- {result}" for result in web_search_results])

    prompt = f"""
    You are an expert financial analyst. Your task is to generate a comprehensive investment report for {stock_name} ({ticker_symbol}).
    Use the provided stock data and recent web search information.

    **Provided Stock Data:**
    {stock_summary_for_llm}

    **Recent Web Search Snippets/Information:**
    {web_summary_for_llm}

    **Report Requirements (Please structure your report with these sections in Markdown format):**

    1.  **Company Overview:**
        * Brief description of the company, its core business, and market position.
        * Mention its sector and industry.

    2.  **Financial Analysis:**
        * Comment on the key financial indicators provided (e.g., P/E ratios, market cap, dividend yield if available).
        * Analyze the recent price trend (from the 1-year history snapshot).
        * Discuss insights from the quarterly financial statements (income, balance sheet, cash flow).
        * Mention any insights from major holders and analyst recommendations.

    3.  **Market Sentiment and News Analysis:**
        * Synthesize insights from the web search snippets.
        * Discuss any recent news, events, or market sentiment that could impact the stock.
        * (If web search snippets are limited, acknowledge this and focus on general market conditions for the sector if possible).

    4.  **Risk Assessment:**
        * Identify potential risks associated with investing in this stock (e.g., industry risks, company-specific risks, market volatility).

    5.  **Opportunities and Growth Drivers:**
        * Identify potential opportunities or growth drivers for the company.

    6.  **Investment Outlook Summary:**
        * Provide a balanced summary of the findings.
        * Conclude with a general outlook for the stock.
        * **Important: Do NOT provide direct financial advice (e.g., "buy," "sell," "hold"). Instead, offer an objective summary of potential upsides and downsides based on the data.**

    Please generate a detailed and well-structured report in Markdown.
    If some data is "Not available" or "Error fetching", acknowledge it and proceed with the available information.
    """

    try:
        st.info("Generating report with LLM... This may take a moment.")
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial analyst AI."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gemma2-9b-it", # Using a powerful Llama 3 model available on Groq. User mentioned llama-3.3-70b-versatile, ensure this is correct or use a known one.
                                   # If "llama-3.3-70b-versatile" is a specific valid model, use that. Otherwise, llama3-70b-8192 is a good choice.
            # model="mixtral-8x7b-32768", # Alternative model if needed
        )
        report = chat_completion.choices[0].message.content
        return report
    except Exception as e:
        st.error(f"Error generating report with Groq API: {e}")
        return f"Failed to generate report: {e}"

# --- Streamlit App UI ---
st.set_page_config(layout="wide", page_title="AI Stock Analyzer")
st.title("📈 AI Powered Stock Analyzer")

st.sidebar.header("Configuration")
if not GROQ_API_KEY_SET:
    st.sidebar.warning("Groq API Key not found. Please set the `GROQ_API_KEY` environment variable.")
    st.sidebar.markdown("You can get a free API key from [Groq Console](https://console.groq.com/keys).")
else:
    st.sidebar.success("Groq API Key loaded.")

st.sidebar.markdown("---")
st.sidebar.header("Enter Stock Details")
ticker_symbol_input = st.sidebar.text_input("Enter Stock Ticker Symbol (e.g., AAPL, MSFT, RELIANCE.NS, BHP.AX):", "AAPL")
# exchange_name_input = st.sidebar.text_input("Optional: Stock Exchange (e.g., NASDAQ, NSE, LSE):", "") # Future use if ticker mapping is implemented

if st.sidebar.button("🔍 Analyze Stock"):
    if not ticker_symbol_input:
        st.error("Please enter a stock ticker symbol.")
    elif not GROQ_API_KEY_SET:
        st.error("Groq API Key is not configured. Cannot generate report.")
    else:
        with st.spinner(f"Fetching data for {ticker_symbol_input}..."):
            stock_data = fetch_stock_data(ticker_symbol_input)

        if stock_data:
            st.header(f"Analysis for: {stock_data['company_name']} ({stock_data['ticker']})")
            
            # Display Stock Data in tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Company Info & Summary", "📈 Price History", "💰 Financials & Holders", "🌐 Web Search (Simulated)"])

            with tab1:
                st.subheader("Company Information")
                st.json(stock_data['info']) # Display the brief info used for LLM
                st.subheader("Business Summary")
                st.markdown(stock_data['summary'])
                st.subheader("Sector & Industry")
                st.write(f"**Sector:** {stock_data['sector']}")
                st.write(f"**Industry:** {stock_data['industry']}")

            with tab2:
                st.subheader("1-Year Stock Price History")
                if stock_data['history_1y'] is not None and not stock_data['history_1y'].empty:
                    st.line_chart(stock_data['history_1y']['Close'])
                    st.dataframe(stock_data['history_1y'].tail())
                else:
                    st.write("Price history not available.")
            
            with tab3:
                st.subheader("Quarterly Financials Summary")
                st.text("Income Statement (Recent):")
                st.text(stock_data['financials_summary']['income_statement_quarterly'])
                st.text("Balance Sheet (Recent):")
                st.text(stock_data['financials_summary']['balance_sheet_quarterly'])
                st.text("Cash Flow (Recent):")
                st.text(stock_data['financials_summary']['cash_flow_quarterly'])

                st.subheader("Major Holders")
                st.text(stock_data['major_holders'])
                st.subheader("Analyst Recommendations (Recent)")
                st.text(stock_data['recommendations'])
            
            # Web Search (Simulated)
            with tab4:
                st.subheader("Simulated Web Search Results")
                with st.spinner(f"Searching web for {stock_data['company_name']}..."):
                    # Using company name for web search
                    web_search_results = search_web_for_stock(stock_data['company_name']) 
                
                if web_search_results:
                    for i, result in enumerate(web_search_results):
                        st.markdown(f"**Result {i+1}:**")
                        st.markdown(result)
                        st.markdown("---")
                else:
                    st.write("No web search results to display.")

            # Generate and Display LLM Report
            st.header("🤖 AI Generated Report")
            with st.spinner("Generating comprehensive report using AI... This might take a few moments."):
                llm_report = generate_report_with_llm(stock_data, web_search_results, stock_data['company_name'], stock_data['ticker'])
            
            st.markdown(llm_report)

            # Optionally display the full yfinance info dump for debugging or more details
            with st.expander("See Full Raw Stock Info (from yfinance)"):
                st.json(stock_data['full_info_dump_for_display'])
        else:
            st.error(f"Could not retrieve data for {ticker_symbol_input}. Please check the ticker symbol and try again.")
else:
    st.info("Enter a stock ticker in the sidebar and click 'Analyze Stock' to begin.")

st.sidebar.markdown("---")
st.sidebar.markdown("Built with Streamlit, yfinance, and Groq.")
st.sidebar.markdown("Note: Financial data provided is for informational purposes only and not investment advice.")

