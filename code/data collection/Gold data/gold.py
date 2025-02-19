import yfinance as yf

# Ticker symbol for Gold Futures
gold_symbol = "GC=F"

# Intervals to fetch data for
intervals = ["1h", "1d", "1wk", "1mo"]  # Hourly, daily, weekly, monthly data

# Loop through each interval
for interval in intervals:
    # Fetch data for Gold Futures
    ticker = yf.Ticker(gold_symbol)
    try:
        data = ticker.history(period="max", interval=interval)  # Fetch max data for each interval
        
        # Export data to CSV
        filename = f"XAU_USD_{interval}_historical_data.csv"
        data.to_csv(filename)
        print(f"Data exported to {filename}")
    except Exception as e:
        print(f"Error fetching data for interval {interval}: {e}")
