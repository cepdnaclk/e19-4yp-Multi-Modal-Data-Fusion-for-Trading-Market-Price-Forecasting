import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from pymongo import MongoClient, ASCENDING
import time

# === MetaTrader 5 Setup ===
if not mt5.initialize():
    print("MetaTrader 5 initialization failed")
    exit()

symbol = "XAUUSD"
timeframe = mt5.TIMEFRAME_M30

# === MongoDB Setup ===
mongo_uri = "mongodb://localhost:27017/"  # Or your Atlas URI
client = MongoClient(mongo_uri)
db = client["market_data"]
collection = db["XAUUSD_M30"]
collection.create_index([("time", ASCENDING)], unique=True)  # avoid duplicates

# === Get Last Stored Timestamp ===
def get_last_mongo_timestamp():
    last = collection.find_one(sort=[("time", -1)])
    if last:
        return last["time"]
    else:
        return datetime(2019, 4, 1)

# === Fetch + Insert Data ===
def fetch_and_store():
    last_time = get_last_mongo_timestamp()
    now = datetime.now()

    # Skip if already up-to-date
    if last_time >= now:
        print("No new data needed.")
        return

    from_ts = int(last_time.timestamp()) + 60  # +60s to avoid overlap
    to_ts = int(now.timestamp())

    rates = mt5.copy_rates_range(symbol, timeframe, from_ts, to_ts)

    if rates is None or len(rates) == 0:
        print("No new data from MT5.")
        return

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")

    records = df.to_dict(orient="records")

    inserted = 0
    for record in records:
        try:
            collection.insert_one(record)
            inserted += 1
        except:
            continue  # Skip if duplicate due to unique index

    print(f"✅ Inserted {inserted} new records from {df['time'].min()} to {df['time'].max()}")

# === Continuous Update Loop ===
try:
    while True:
        fetch_and_store()
        time.sleep(10)  # check every 10 seconds
except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    mt5.shutdown()
