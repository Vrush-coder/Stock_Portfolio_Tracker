import requests
import json
import matplotlib.pyplot as plt
import yfinance as yf

# Fetch data for a stock symbol (e.g., AAPL for Apple)
stock = yf.Ticker('AAPL')

# Get historical market data
data = stock.history(period='5d')
print(data)

class StockPortfolio:
    def __init__(self, data_file="portfolio.json"):
        self.data_file = data_file
        try:
            with open(data_file, 'r') as file:
                self.portfolio = json.load(file)
        except FileNotFoundError:
            self.portfolio = []

    def save_portfolio(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.portfolio, file, indent=4)

    def add_stock(self, ticker, quantity, purchase_price):
        stock = {
            'ticker': ticker.upper(),
            'quantity': quantity,
            'purchase_price': purchase_price
        }
        self.portfolio.append(stock)
        self.save_portfolio()
        print(f"Added {ticker.upper()} to your portfolio.")

    def remove_stock(self, ticker):
        self.portfolio = [stock for stock in self.portfolio if stock['ticker'] != ticker.upper()]
        self.save_portfolio()
        print(f"Removed {ticker.upper()} from your portfolio.")

    def fetch_stock_price(self, ticker):
        API_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo"
        API_KEY = "CR6KXM234DEX6WJ3"  # Replace with your API key'
        try:
            response = requests.get(API_URL, params={
                "function": "GLOBAL_QUOTE",
                "symbol": "IBM",
                "apikey": API_KEY
            })
            response.raise_for_status()  # Raise HTTPError for bad responses
            data = response.json()
            if "Global Quote" in data and "05. price" in data["Global Quote"]:
                return float(data["Global Quote"]["05. price"])
            else:
                print(f"Invalid response for ticker {ticker}: {data}")
                return None
        except Exception as e:
            print(f"Error fetching price for {ticker}: {e}")
            return None

    def calculate_portfolio_performance(self):
        total_investment = 0
        total_current_value = 0
        stock_values = []  # To store current value of each stock
        stock_labels = []  # To store stock tickers for labeling
        
        print("\nYour Portfolio Performance:\n")
        for stock in self.portfolio:
            current_price = self.fetch_stock_price(stock['ticker'])
            if current_price is not None:
                current_value = current_price * stock['quantity']
                total_investment += stock['purchase_price'] * stock['quantity']
                total_current_value += current_value
                stock_values.append(current_value)
                stock_labels.append(stock['ticker'])
                print(f"{stock['ticker']} | Quantity: {stock['quantity']} | Purchase Price: ${stock['purchase_price']} | "
                      f"Current Price: ${current_price:.2f} | Current Value: ${current_value:.2f}")
            else:
                print(f"Unable to fetch current price for {stock['ticker']}.")

        print("\nSummary:")
        print(f"Total Investment: ${total_investment:.2f}")
        print(f"Total Current Value: ${total_current_value:.2f}")
        print(f"Net Gain/Loss: ${total_current_value - total_investment:.2f}")
        
        # Graphical Representation using matplotlib
        self.plot_graph(stock_labels, stock_values, total_investment, total_current_value)

    def plot_graph(self, stock_labels, stock_values, total_investment, total_current_value):
        # Bar graph showing current value of each stock
        plt.figure(figsize=(10, 6))
        plt.bar(stock_labels, stock_values, color='green', label="Current Value")
        plt.title("Stock Portfolio - Current Value of Each Stock")
        plt.xlabel("Stock Ticker")
        plt.ylabel("Current Value ($)")
        plt.show()

        # Pie chart showing portfolio distribution
        plt.figure(figsize=(8, 8))
        plt.pie(stock_values, labels=stock_labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title("Portfolio Distribution by Stock Value")
        plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
        plt.show()

        # Bar graph comparing total investment vs. current value of portfolio
        plt.figure(figsize=(6, 6))
        plt.bar(["Total Investment", "Total Current Value"], [total_investment, total_current_value], color=['blue', 'orange'])
        plt.title("Total Investment vs. Total Current Value")
        plt.ylabel("Amount ($)")
        plt.show()

def menu():
    portfolio = StockPortfolio()
    while True:
        print("\n--- Stock Portfolio Tracker ---")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio Performance")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            ticker = input("Enter stock ticker: ").strip()
            quantity = int(input("Enter quantity: "))
            purchase_price = float(input("Enter purchase price per share: "))
            portfolio.add_stock(ticker, quantity, purchase_price)
        elif choice == "2":
            ticker = input("Enter stock ticker to remove: ").strip()
            portfolio.remove_stock(ticker)
        elif choice == "3":
            portfolio.calculate_portfolio_performance()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
