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
end_time = datetime.now()  # Fetch data up to the current time
chunk_size_days = 365  # Fetch data in 1-year chunks
all_data = pd.DataFrame()

print(f"Fetching available data for {symbol}...")

while True:
    try:
        # Calculate the chunk start time
        start_time = end_time - timedelta(days=chunk_size_days)

        # Fetch rates for this chunk
        rates = mt5.copy_rates_range(
            symbol,
            timeframe,
            int(start_time.timestamp()),
            int(end_time.timestamp())
        )

        if rates is None or len(rates) == 0:
            print(f"No more data available from {start_time} to {end_time}.")
            break

        # Convert to DataFrame
        columns = ["time", "open", "high", "low", "close", "tick_volume"]
        chunk_data = pd.DataFrame(rates, columns=columns)
        chunk_data["time"] = pd.to_datetime(chunk_data["time"], unit="s")

        # Append to all_data
        all_data = pd.concat([chunk_data, all_data], ignore_index=True)

        # Update the end_time for the next iteration
        end_time = start_time
        print(f"Fetched {len(chunk_data)} records from {start_time} to {end_time}.")
    except OSError as e:
        print(f"An error occurred: {e}")
        break

# Shutdown MetaTrader connection
mt5.shutdown()

if all_data.empty:
    print(f"No data available for {symbol}. Exiting.")
    exit()

# Save data to CSV
output_filename = f"{symbol}_30m_all_data_new.csv"
all_data.to_csv(output_filename, index=False)
print(f"Data saved to {output_filename}.")
