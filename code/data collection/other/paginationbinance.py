import requests
import pandas as pd
from datetime import datetime

# Parameters
base_url = "https://api.binance.com"
symbol = "BTCUSDT"
interval = "4h"
limit = 500  # Max records per request

# Define start time (e.g., timestamp for 1 Jan 2020)
start_time = int(datetime(2020, 1, 1).timestamp() * 1000)  # Convert to ms
all_data = []

while True:
    url = f"{base_url}/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}&startTime={start_time}"
    response = requests.get(url)
    data = response.json()
    
    if not data:
        break  # No more data

    all_data.extend(data)

    # Update the start_time to the next period
    start_time = data[-1][6] + 1  # Last close time + 1 ms

# Convert to Pandas DataFrame
df = pd.DataFrame(all_data, columns=["Open Time", "Open", "High", "Low", "Close", "Volume",
                                     "Close Time", "Quote Asset Volume", "Number of Trades",
                                     "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore"])

# Convert timestamps to readable date-time formats
df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')

# Save to CSV
df.to_csv("BTC_4h_binance_data.csv", index=False)
