import yfinance as yf

# List of cryptocurrency pairs
cryptos = ["BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "SOL-USD", 
           "XRP-USD", "DOGE-USD", "DOT-USD", "LTC-USD", "AVAX-USD"]

# Intervals to fetch data for
intervals = ["1h","1d", "1wk", "1mo"]  # Example: hourly, daily, weekly, monthly data

for crypto in cryptos:
    for interval in intervals:
        # Fetch data for each interval
        ticker = yf.Ticker(crypto)
        data = ticker.history(period="max", interval=interval)
        
        # Export to CSV
        filename = f"{crypto}_{interval}_historical_data.csv"
        data.to_csv(filename)
        print(f"Data exported to {filename}")
