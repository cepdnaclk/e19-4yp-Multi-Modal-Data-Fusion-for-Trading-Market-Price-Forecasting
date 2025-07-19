import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from pymongo import MongoClient, ASCENDING

# -----------------------------------------------------------------------------
# 1) Initialize MT5
# -----------------------------------------------------------------------------
if not mt5.initialize():
    print("MetaTrader5 initialization failed!")
    quit()

symbol    = "XAUUSD"
timeframe = mt5.TIMEFRAME_M30

# -----------------------------------------------------------------------------
# 2) Connect to MongoDB Atlas
#    Replace YourPasswordHere with your actual Atlas user password.
# -----------------------------------------------------------------------------
client = MongoClient(
    "mongodb+srv://nuwanthalakshan919:vAF9gE6T4KIM5GF8"
    "@cluster0.6pbneot.mongodb.net/market_data"
    "?retryWrites=true&w=majority"
)
db         = client["market_data"]
collection = db["XAUUSD_M30"]
# create unique index on time to avoid duplicates
collection.create_index([("time", ASCENDING)], unique=True)

# -----------------------------------------------------------------------------
# 3) Define the time range for the initial data pull
# -----------------------------------------------------------------------------
start_time = datetime(2021, 1, 1)
end_time   = datetime.utcnow()

# -----------------------------------------------------------------------------
# 4) Fetch historical bars from MT5
# -----------------------------------------------------------------------------
rates = mt5.copy_rates_range(symbol, timeframe, start_time, end_time)
if rates is None or len(rates) == 0:
    print("No data returned from MT5 for the specified date range.")
    mt5.shutdown()
    quit()

# -----------------------------------------------------------------------------
# 5) Convert to DataFrame & insert into MongoDB Atlas
# -----------------------------------------------------------------------------
df = pd.DataFrame(rates)
df["time"] = pd.to_datetime(df["time"], unit="s")

inserted = 0
for record in df.to_dict(orient="records"):
    try:
        collection.insert_one(record)
        inserted += 1
    except Exception:
        # duplicate key on 'time' or other insert error: skip
        continue

print(f"Inserted {inserted} records from {start_time} to {end_time}.")

# -----------------------------------------------------------------------------
# 6) Clean up
# -----------------------------------------------------------------------------
mt5.shutdown()