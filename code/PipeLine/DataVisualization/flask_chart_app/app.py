from flask import Flask, render_template, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

def get_data(limit=500):
    conn = sqlite3.connect('market_data.db')
    df = pd.read_sql_query(
        "SELECT time, close FROM XAUUSD_M30 ORDER BY time DESC LIMIT ?", conn, params=(limit,))
    conn.close()
    df = df.sort_values('time')  # ascending order
    df['time'] = pd.to_datetime(df['time']).astype(str)
    return df

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/price-data")
def price_data():
    df = get_data()
    return jsonify({
        "time": df["time"].tolist(),
        "close": df["close"].tolist()
    })

if __name__ == "__main__":
    app.run(debug=True)
