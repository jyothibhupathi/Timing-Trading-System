# data_fetching.py
import yfinance as yf

def fetch_data(ticker_symbol, duration='1mo', time_interval='1d'):
    """
    Fetch stock data using yfinance.
    
    Args:
    - ticker_symbol (str): The stock ticker symbol.
    - duration (str): The period of data to fetch (default is '1mo').
    - time_interval (str): The interval of the data (default is '1d').
    
    Returns:
    - DataFrame: Stock data.
    """
    try:
        stock_df = yf.download(ticker_symbol, period=duration, interval=time_interval)
        return stock_df
    except Exception as err:
        print(f"Error while fetching data: {err}")
        return None
