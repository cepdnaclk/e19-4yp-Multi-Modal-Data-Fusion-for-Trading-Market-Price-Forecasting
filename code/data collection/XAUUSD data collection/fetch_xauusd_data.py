import yfinance as yf

# Fetch XAU/USD data (gold price)
xauusd = yf.download('XAUUSD=X', interval="30m", start="2018-01-01")
xauusd.to_csv("XAUUSD_30m_historical_data.csv")
print("XAU/USD data saved!")
