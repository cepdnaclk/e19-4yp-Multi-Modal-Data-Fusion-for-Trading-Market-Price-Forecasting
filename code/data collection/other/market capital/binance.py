import requests
import pandas as pd
from datetime import datetime, timedelta

# Function to fetch the BTC price from Binance
def fetch_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {
        'symbol': 'BTCUSDT'  # Get BTC price against USDT
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return float(data['price'])
    else:
        print("Error fetching BTC price from Binance.")
        return None

# Function to fetch the circulating supply of Bitcoin from CoinGecko
def fetch_btc_supply():
    gecko_url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    response = requests.get(gecko_url)
    if response.status_code == 200:
        data = response.json()
        return data['market_data']['circulating_supply']
    else:
        print("Error fetching Bitcoin circulating supply.")
        return None

# Function to calculate the BTC market cap
def calculate_market_cap(price, supply):
    return price * supply

# Function to get market cap data over a range of dates
def get_btc_market_cap_data(start_date, end_date):
    # Create an empty list to store the market cap data
    market_cap_data = []
    
    # Loop over each day from start_date to end_date
    current_date = start_date
    while current_date <= end_date:
        print(f"Fetching data for {current_date.strftime('%Y-%m-%d')}")

        # Fetch BTC price and supply for the current day
        btc_price = fetch_btc_price()
        btc_supply = fetch_btc_supply()

        # Calculate the market cap if both price and supply are available
        if btc_price and btc_supply:
            market_cap = calculate_market_cap(btc_price, btc_supply)
            market_cap_data.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'BTC Price (USD)': btc_price,
                'BTC Circulating Supply': btc_supply,
                'BTC Market Cap (USD)': market_cap
            })
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    return market_cap_data

# Start and end dates for the range (for example, the last 30 days)
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=30)  # Last 30 days

# Get BTC market cap data for the specified range
btc_market_cap_data = get_btc_market_cap_data(start_date, end_date)

# Convert the data to a pandas DataFrame
if btc_market_cap_data:
    df = pd.DataFrame(btc_market_cap_data)
    print(df)

    # Save data to a CSV file
    df.to_csv('btc_market_cap.csv', index=False)
    print("BTC market cap data has been saved to 'btc_market_cap.csv'.")
else:
    print("No data to save.")
