# indicators.py
import pandas as pd

def compute_indicators(stock_data):
    """
    Compute technical indicators for stock data.
    
    Args:
    - stock_data (DataFrame): DataFrame containing stock data.
    
    Returns:
    - DataFrame: Stock data with RSI and MACD indicators.
    """
    # Calculate Relative Strength Index (RSI)
    price_change = stock_data['Close'].diff()
    avg_gain = (price_change.where(price_change > 0, 0)).rolling(window=14).mean()
    avg_loss = (-price_change.where(price_change < 0, 0)).rolling(window=14).mean()
    relative_strength = avg_gain / avg_loss
    stock_data['RSI'] = 100 - (100 / (1 + relative_strength))

    # Calculate Moving Average Convergence Divergence (MACD)
    stock_data['EMA_12'] = stock_data['Close'].ewm(span=12, adjust=False).mean()
    stock_data['EMA_26'] = stock_data['Close'].ewm(span=26, adjust=False).mean()
    stock_data['MACD_Line'] = stock_data['EMA_12'] - stock_data['EMA_26']
    stock_data['Signal_Line'] = stock_data['MACD_Line'].ewm(span=9, adjust=False).mean()

    return stock_data
