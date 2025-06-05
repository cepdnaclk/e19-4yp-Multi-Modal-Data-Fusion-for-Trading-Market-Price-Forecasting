import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta

# Initialize MetaTrader connection
if not mt5.initialize():
    print("MetaTrader 5 initialization failed")
    mt5.shutdown()
    exit()

# Define parameters
symbol = "XAUUSD"
timeframe = mt5.TIMEFRAME_M30  # 30-minute timeframe
start_time = datetime(2018, 1, 1)  # Start from this date
end_time = datetime.now()  # Up to now
chunk_size_days = 365  # Fetch in 1-year chunks
all_data = pd.DataFrame()

print(f"Fetching {symbol} data from {start_time} to {end_time}...")

while start_time < end_time:
    try:
        chunk_end_time = min(start_time + timedelta(days=chunk_size_days), end_time)

        # Fetch data for this time chunk
        rates = mt5.copy_rates_range(
            symbol,
            timeframe,
            int(start_time.timestamp()),
            int(chunk_end_time.timestamp())
        )

        if rates is None or len(rates) == 0:
            print(f"No data found from {start_time} to {chunk_end_time}")
        else:
            # Convert to DataFrame
            columns = ["time", "open", "high", "low", "close", "tick_volume"]
            chunk_data = pd.DataFrame(rates, columns=columns)
            chunk_data["time"] = pd.to_datetime(chunk_data["time"], unit="s")

            all_data = pd.concat([all_data, chunk_data], ignore_index=True)
            print(f"Fetched {len(chunk_data)} records from {start_time} to {chunk_end_time}.")

        start_time = chunk_end_time  # Move to next chunk

    except OSError as e:
        print(f"An error occurred: {e}")
        break

# Shutdown MetaTrader connection
mt5.shutdown()

if all_data.empty:
    print(f"No data available for {symbol}. Exiting.")
    exit()

# Save to CSV
output_filename = f"{symbol}_30m_from_2018.csv"
all_data.to_csv(output_filename, index=False)
print(f"✅ Data saved to {output_filename}")

