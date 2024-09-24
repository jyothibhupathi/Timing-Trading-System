# ui.py
import matplotlib.pyplot as plt
import openai
from data_fetching import fetch_data
from indicators import compute_indicators

# Set OpenAI API Key
openai.api_key = "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"

def show_main_menu():
    """
    Display the main menu for stock analysis.
    """
    print("Welcome to the Stock Analysis Tool!")
    print("Available Stocks:")
    print("1. NFLX (Netflix)")
    print("2. DIS (Walt Disney)")
    print("3. NVDA (NVIDIA)")
    print("4. FB (Meta Platforms)")
    print("5. AMD (Advanced Micro Devices)")

def plot_stock_data(stock_data, selected_ticker):
    """
    Plot stock data along with indicators.
    
    Args:
    - stock_data (DataFrame): DataFrame containing stock data with indicators.
    - selected_ticker (str): The selected stock ticker.
    """
    plt.figure(figsize=(14, 10))

    # Plot Close Price
    plt.subplot(3, 1, 1)
    plt.plot(stock_data['Close'], label='Close Price', color='blue')
    plt.title(f'{selected_ticker} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    # Plot RSI
    plt.subplot(3, 1, 2)
    plt.plot(stock_data['RSI'], label='RSI', color='orange')
    plt.axhline(70, linestyle='--', color='red', label='Overbought (70)')
    plt.axhline(30, linestyle='--', color='green', label='Oversold (30)')
    plt.title('Relative Strength Index (RSI)')
    plt.legend()

    # Plot MACD
    plt.subplot(3, 1, 3)
    plt.plot(stock_data['MACD_Line'], label='MACD', color='purple')
    plt.plot(stock_data['Signal_Line'], label='Signal Line', color='red')
    plt.title('MACD')
    plt.xlabel('Date')
    plt.legend()

    plt.tight_layout()
    plt.show()

def main():
    """
    Main function to run the stock analysis tool.
    """
    while True:
        show_main_menu()
        stock_selection = input("Select a stock by number: ")
        stock_tickers = ['NFLX', 'DIS', 'NVDA', 'FB', 'AMD']
        selected_ticker = stock_tickers[int(stock_selection) - 1]

        print("\nSelect a time interval for analysis:")
        print("1. 1 Minute (Period: 1d)")
        print("2. 5 Minutes (Period: 1d)")
        print("3. 1 Hour (Period: 1d or 5d)")
        print("4. 1 Day (Period: 5d, 1mo)")
        print("5. 1 Week (Period: 1mo, 3mo)")
        interval_selection = input("Choose an option (1-5): ")
        time_intervals = ['1m', '5m', '1h', '1d', '1wk']
        period_choice = '1d' if interval_selection in ['1', '2', '3'] else '1mo'
        chosen_interval = time_intervals[int(interval_selection) - 1]

        # Fetch stock data
        stock_data = fetch_data(selected_ticker, period_choice, chosen_interval)
        if stock_data is not None:
            stock_data = compute_indicators(stock_data)
            plot_stock_data(stock_data, selected_ticker)

            # Trading decision
            trading_decision = input("Would you like to trade? (buy/sell/exit): ").strip().lower()
            if trading_decision in ['buy', 'sell']:
                ai_response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f"Provide trading suggestions for {trading_decision}ing {selected_ticker}.",
                    max_tokens=50
                )
                print(f"AI Suggestion: {ai_response.choices[0].text.strip()}")
            elif trading_decision == 'exit':
                print("Exiting the program.")
                break

if __name__ == "__main__":
    main()
