import requests
import pandas as pd

# Alpha Vantage API setup
API_KEY = 'your_alpha_vantage_api_key'  # Replace with your valid API key
from_symbol = "XAU"
to_symbol = "USD"
interval = "30min"
output_size = "full"

# URL for API request
url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={from_symbol}&to_symbol={to_symbol}&interval={interval}&outputsize={output_size}&apikey={API_KEY}"

# Fetch data
response = requests.get(url)

# Debug API response
print("Response Status Code:", response.status_code)  # Check HTTP response code
print("Response JSON:", response.json())  # Output the entire JSON

# Process data
data = response.json()
if "Time Series FX (30min)" in data:
    df = pd.DataFrame.from_dict(data["Time Series FX (30min)"], orient="index", dtype=float)
    df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close"
    }, inplace=True)

    # Format and save
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    df.to_csv(f"{from_symbol}{to_symbol}_30min_historical_data.csv")
    print(f"Data saved to {from_symbol}{to_symbol}_30min_historical_data.csv")
else:
    print(f"Error: {data.get('Error Message', 'Failed to fetch data')}")
