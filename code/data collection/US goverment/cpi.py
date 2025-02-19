import requests
import pandas as pd
from datetime import datetime, timedelta

# Your FRED API Key
API_KEY = 'f32c136c236b7027930be78be9a65a5c'

# Base URL
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

# Series IDs for CPI and NFP
series = {
    "CPI": "CPIAUCSL",
    "NFP": "NFP"
}

# Define the start and end dates for the past 3 years
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=3*365)).strftime("%Y-%m-%d")

def fetch_data(series_id, start_date, end_date, api_key):
    # Construct the API URL
    url = f"{BASE_URL}?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={start_date}&observation_end={end_date}"
    
    # Make the API request
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        observations = data.get("observations", [])
        return observations
    else:
        print(f"Error fetching data for series ID: {series_id}, Status Code: {response.status_code}")
        return []

def save_to_csv(data, filename):
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    
    if not df.empty:
        # Only keep relevant columns
        df = df[['date', 'value']]
        df.columns = ['Date', 'Value']
        
        # Save to CSV
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print(f"No data to save for {filename}")

# Fetch and save data for both CPI and NFP
for name, series_id in series.items():
    print(f"Fetching data for {name}...")
    data = fetch_data(series_id, start_date, end_date, API_KEY)
    save_to_csv(data, f"{name}_data.csv")
