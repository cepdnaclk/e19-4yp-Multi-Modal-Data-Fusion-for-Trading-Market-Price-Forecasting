import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from pymongo import MongoClient, ASCENDING
import time

# === 1. Initialize MT5 ===
if not mt5.initialize():
    print("❌ MetaTrader5 initialization failed!")
    quit()

symbol = "XAUUSD"
timeframe = mt5.TIMEFRAME_M30

# === 2. Connect to MongoDB ===
client = MongoClient("mongodb://localhost:27017/")
db = client["market_data"]
collection = db["XAUUSD_M30"]
collection.create_index([("time", ASCENDING)], unique=True)

def fetch_and_insert_new():
    # Get the last inserted timestamp from DB
    last_doc = collection.find_one(sort=[("time", -1)])
    last_time = last_doc["time"] if last_doc else datetime(2019, 4, 1)
    
    now = datetime.now()
    from_ts = int(last_time.timestamp()) + 60  # +60 seconds to avoid overlap
    to_ts = int(now.timestamp())
    
    # If no new time range, just return
    if from_ts >= to_ts:
        print("No new data to fetch.")
        return
    
    # Fetch new data from MT5
    rates = mt5.copy_rates_range(symbol, timeframe, from_ts, to_ts)
    
    if rates is None or len(rates) == 0:
        print("No new data returned from MT5.")
        return
    
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    
    inserted = 0
    for record in df.to_dict(orient="records"):
        try:
            collection.insert_one(record)
            inserted += 1
        except Exception:
            continue  # Duplicate time, skip
    
    print(f"Inserted {inserted} new records from {df['time'].min()} to {df['time'].max()}")

try:
    # Run initial bulk insert first (optional: you can skip if already done)
    # fetch_and_insert_new()  # Uncomment if you want to fetch any data missed before

    # Continuous polling every 10 seconds
    while True:
        fetch_and_insert_new()
        time.sleep(10)

except KeyboardInterrupt:
    print("Process stopped by user.")
finally:
    mt5.shutdown()
