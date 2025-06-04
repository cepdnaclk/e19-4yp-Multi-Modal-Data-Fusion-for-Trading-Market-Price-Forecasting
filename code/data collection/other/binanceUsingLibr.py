import ccxt
import pandas as pd
import time

# Initialize Binance client
exchange = ccxt.binance()

# Define parameters
symbol = "BTC/USDT"  # Pair to fetch
timeframe = "30m"  # 30-minute time frame
since = exchange.parse8601("2018-01-01T00:00:00Z")  # Start from Jan 1, 2018

# Fetch historical data
all_data = []
limit = 1000  # Binance limit for candles per request
while True:
    print(f"Fetching data from: {exchange.iso8601(since)}")
    data = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
    if len(data) == 0:
        break
    all_data += data
    # Move the starting point forward to avoid overlap
    since = data[-1][0] + 1
    time.sleep(1)  # Avoid hitting rate limits

# Convert to DataFrame
columns = ["timestamp", "open", "high", "low", "close", "volume"]
df = pd.DataFrame(all_data, columns=columns)

# Format and save to CSV
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
df.set_index("timestamp", inplace=True)
df.to_csv("BTCUSDT_30m_historical_data.csv")

print(f"Data saved to BTCUSDT_30m_historical_data.csv")
