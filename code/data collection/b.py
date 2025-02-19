import requests
import pandas as pd
from datetime import datetime

# Binance API endpoint and parameters
base_url = "https://api.binance.com"
symbol = "BTCUSDT"  # Trading pair (Bitcoin to USDT)
interval = "30m"  # Time interval: 1m, 1h, 1d, etc.
limit = 1000         # Number of data points to fetch (max: 1000)

# Construct the URL and fetch data
url = f"{base_url}/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
response = requests.get(url)
data = response.json()

# Extract data into a list of dictionaries for easy handling
candlestick_data = []
for entry in data:
    candlestick_data.append({
        "Open Time": datetime.utcfromtimestamp(entry[0] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # Convert milliseconds to datetime
        "Open Price": float(entry[1]),
        "High Price": float(entry[2]),
        # "Low Price": float(entry[3]),
        # "Close Price": float(entry[4]),
        # "Volume": float(entry[5]),
        # "Close Time": datetime.utcfromtimestamp(entry[6] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
        # "Quote Asset Volume": float(entry[7]),
        # "Number of Trades": int(entry[8]),
        # "Taker Buy Base Asset Volume": float(entry[9]),
        # "Taker Buy Quote Asset Volume": float(entry[10]),
    })

# Convert the data into a Pandas DataFrame
df = pd.DataFrame(candlestick_data)

# Save the DataFrame to a CSV file
output_file = "binance_candlestick_datafor_30min.csv"
df.to_csv(output_file, index=False)
print(f"Data saved to {output_file}")

# Optional: Display the first few rows of the DataFrame
print(df.head())
