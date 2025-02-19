import yfinance as yf

# Fetch EUR/USD data
eurusd = yf.download('EURUSD=X', interval="30m", start="2018-01-01")
eurusd.to_csv("EURUSD_30m_historical_data.csv")
print("EUR/USD data saved!")

# Fetch XAU/USD data (gold price)
xauusd = yf.download('XAUUSD=X', interval="30m", start="2018-01-01")
xauusd.to_csv("XAUUSD_30m_historical_data.csv")
print("XAU/USD data saved!")
