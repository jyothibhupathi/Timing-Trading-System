import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openai

# OpenAI API Key
openai.api_key = "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"

# Data Fetching
def fetch_stock_data(ticker, period='1mo', interval='1d'):
    try:
        stock_data = yf.download(ticker, period=period, interval=interval)
        return stock_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Indicator Calculations
def calculate_indicators(data):
    # Calculate RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Calculate MACD
    data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = data['EMA_12'] - data['EMA_26']
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

    return data

# User Interface
def display_menu():
    print("Welcome to the Stock Analysis Tool!")
    print("Available Stocks:")
    print("1. NFLX (Netflix)")
    print("2. DIS (Walt Disney)")
    print("3. NVDA (NVIDIA)")
    print("4. FB (Meta Platforms)")
    print("5. AMD (Advanced Micro Devices)")

def main():
    while True:
        display_menu()
        stock_choice = input("Choose a stock by number: ")
        stock_tickers = ['NFLX', 'DIS', 'NVDA', 'FB', 'AMD']
        ticker = stock_tickers[int(stock_choice) - 1]

        print("\nChoose a time interval for analysis:")
        print("1. 1 Minute (Period: 1d)")
        print("2. 5 Minutes (Period: 1d)")
        print("3. 1 Hour (Period: 1d or 5d)")
        print("4. 1 Day (Period: 5d, 1mo)")
        print("5. 1 Week (Period: 1mo, 3mo)")
        interval_choice = input("Choose an option (1-5): ")
        intervals = ['1m', '5m', '1h', '1d', '1wk']
        period = '1d' if interval_choice in ['1', '2', '3'] else '1mo'
        interval = intervals[int(interval_choice) - 1]

        # Fetch stock data
        data = fetch_stock_data(ticker, period, interval)
        if data is not None:
            data = calculate_indicators(data)

            # Plotting
            plt.figure(figsize=(14, 10))

            # Plot Close Price
            plt.subplot(3, 1, 1)
            plt.plot(data['Close'], label='Close Price', color='blue')
            plt.title(f'{ticker} Stock Price')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.legend()

            # Plot RSI
            plt.subplot(3, 1, 2)
            plt.plot(data['RSI'], label='RSI', color='orange')
            plt.axhline(70, linestyle='--', color='red', label='Overbought (70)')
            plt.axhline(30, linestyle='--', color='green', label='Oversold (30)')
            plt.title('Relative Strength Index (RSI)')
            plt.legend()

            # Plot MACD
            plt.subplot(3, 1, 3)
            plt.plot(data['MACD'], label='MACD', color='purple')
            plt.plot(data['Signal_Line'], label='Signal Line', color='red')
            plt.title('MACD')
            plt.xlabel('Date')
            plt.legend()

            plt.tight_layout()
            plt.show()

            # Trading decision
            trade_choice = input("Do you want to trade? (buy/sell/exit): ").strip().lower()
            if trade_choice in ['buy', 'sell']:
                suggestion = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f"Provide trading suggestions for {trade_choice}ing {ticker}.",
                    max_tokens=50
                )
                print(f"AI Suggestion: {suggestion.choices[0].text.strip()}")
            elif trade_choice == 'exit':
                print("Exiting the program.")
                break

if __name__ == "__main__":
    main()
