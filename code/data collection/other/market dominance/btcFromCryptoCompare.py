import requests
import pandas as pd
from datetime import datetime

api_key = '40b915854f083c7869c7d4b4bc1d6f920e22ff1c768af1dffce1ccb3d2022a4f'
url = "https://min-api.cryptocompare.com/data/v2/histoday"

# Fetch data for BTC market cap
params_btc = {
    'fsym': 'BTC',
    'tsym': 'USD',
    'limit': 2000,  # Number of data points for the time frame
    'toTs': int(datetime.now().timestamp())  # Adjust date range as needed
}

# Function to fetch and check response data
def fetch_data(url, params):
    print("Fetching data with parameters:", params)  # Debug: print params being used
    response = requests.get(url, params=params, headers={'Authorization': f'Apikey {api_key}'})
    if response.status_code == 200:
        print("Successfully fetched data from the API.")  # Debug: confirm successful API response
        return response.json()
    else:
        print("Error fetching data, status code:", response.status_code)  # Debug: print status code if fails
        return None

# Get BTC market cap data
btc_data = fetch_data(url, params_btc)

# Check if BTC data is valid
if btc_data and 'Data' in btc_data:
    print("BTC Data found.")  # Debug: BTC data available

    btc_market_cap_data = []

    # Iterate through the data and store BTC market cap
    for btc_item in btc_data['Data']['Data']:
        timestamp = datetime.utcfromtimestamp(btc_item['time'])
        btc_market_cap = btc_item['close']  # Close price as an approximation for market cap
        
        # Add BTC market cap to the list for export
        btc_market_cap_data.append([timestamp.strftime('%Y-%m-%d'), btc_market_cap])

    # Save BTC market cap data to CSV
    if btc_market_cap_data:
        try:
            # Convert BTC market cap data into a pandas DataFrame
            df_btc_market_cap = pd.DataFrame(btc_market_cap_data, columns=['Date', 'BTC Market Cap'])

            # Save the BTC market cap DataFrame to a CSV file
            market_cap_file_path = 'btc_market_cap_hist_year.csv'
            df_btc_market_cap.to_csv(market_cap_file_path, index=False)
            print("BTC Market Cap data has been successfully saved to 'btc_market_cap_hist_year.csv'.")  # Debug: Confirmation after saving BTC market cap data

        except Exception as e:
            print("Error occurred while saving BTC Market Cap data:", e)  # Debug: print any errors during saving BTC market cap data
else:
    print("BTC data is unavailable or invalid.")  # Debug: BTC data is missing or invalid
