import yfinance as yf

# List of cryptocurrency pairs
cryptos = ["BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "SOL-USD", 
           "XRP-USD", "DOGE-USD", "DOT-USD", "LTC-USD", "AVAX-USD"]

for crypto in cryptos:
    # Fetch data
    ticker = yf.Ticker(crypto)
    data = ticker.history(period="max")
    
    # Export to CSV
    filename = f"{crypto}_historical_data.csv"
    data.to_csv(filename)
    print(f"Data exported to {filename}")
