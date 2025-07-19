import time
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
from pymongo import MongoClient, ASCENDING

# --- INITIAL SETUP (run once) ---
if not mt5.initialize():
    raise RuntimeError("MetaTrader5 initialization failed!")

symbol    = "XAUUSD"
timeframe = mt5.TIMEFRAME_M30

client   = MongoClient("mongodb://localhost:27017/")
db       = client["market_data"]
col      = db["XAUUSD_M30"]
# ensure unique index on time so duplicates are skipped
col.create_index([("time", ASCENDING)], unique=True)

# --- HELPER TO GET LAST TIMESTAMP ---
def get_last_time():
    doc = col.find_one(sort=[("time", -1)])
    if doc:
        return doc["time"]
    else:
        # if no data, start from Jan 1, 2021
        return datetime(2021, 1, 1)

# --- MAIN POLLING LOOP ---
def run_realtime_sync(poll_interval=30):
    last_time = get_last_time()
    print(f"Starting sync from {last_time}")
    try:
        while True:
            # MT5 wants UTC timestamps; our Mongo times are timezone‐naive UTC
            # fetch a bit before last_time to avoid gaps (but unique index skips exact duplicates)
            fetch_from = last_time - timedelta(seconds=1)
            # fetch up to 'now'
            now = datetime.utcnow()
            rates = mt5.copy_rates_range(symbol, timeframe, fetch_from, now)
            if rates is not None and len(rates) > 0:
                df = pd.DataFrame(rates)
                df["time"] = pd.to_datetime(df["time"], unit="s")
                inserted = 0
                for rec in df.to_dict(orient="records"):
                    try:
                        col.insert_one(rec)
                        inserted += 1
                        # update last_time only when we successfully insert a newer bar
                        if rec["time"] > last_time:
                            last_time = rec["time"]
                    except Exception:
                        # duplicate or other error: skip
                        pass
                if inserted:
                    print(f"[{datetime.utcnow()}] Inserted {inserted} new bars, latest at {last_time}")
            else:
                print(f"[{datetime.utcnow()}] No new bars since {last_time}")
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("Stopping real‑time sync.")
    finally:
        mt5.shutdown()

if __name__ == "__main__":
    run_realtime_sync()