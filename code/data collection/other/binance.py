import requests
from datetime import datetime

# Binance API endpoint and parameters
base_url = "https://api.binance.com"
symbol = "BTCUSDT"
interval = "30m"  # Time interval: 1m, 1h, 1d, etc.
limit = 2000  # Number of data points to fetch

# Construct the URL and fetch data
url = f"{base_url}/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
response = requests.get(url)
data = response.json()

# Print formatted time along with open and close prices
for entry in data:
    # Convert the timestamp from milliseconds to seconds, and then to a human-readable datetime
    timestamp = int(entry[0]) / 1000  # entry[0] is the timestamp in milliseconds
    readable_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')  # UTC time
    print(f"Time: {readable_time} UTC, Open: {entry[1]}, Close: {entry[4]}")
