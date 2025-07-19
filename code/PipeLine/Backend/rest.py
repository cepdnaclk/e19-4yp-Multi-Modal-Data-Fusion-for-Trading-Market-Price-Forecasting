from flask import Flask, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)
DB_FILENAME = "market_data.db"

@app.route("/api/price-data")
def price_data():
    conn = sqlite3.connect(DB_FILENAME)
    df = pd.read_sql_query("SELECT * FROM XAUUSD_M30 ORDER BY time DESC", conn)
    conn.close()
    
    # Convert timestamp string to milliseconds since epoch (for JS Date)
    df['time'] = pd.to_datetime(df['time'])
    data = df.apply(lambda row: [int(row['time'].timestamp() * 1000), row['close']], axis=1).tolist()
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
