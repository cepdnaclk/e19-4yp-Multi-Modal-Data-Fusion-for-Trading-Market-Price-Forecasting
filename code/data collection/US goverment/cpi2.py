import requests
import pandas as pd
from datetime import datetime, timedelta

# Your FRED API Key
API_KEY = 'f32c136c236b7027930be78be9a65a5c'

# Base URL for FRED API
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

# CPI Series ID
CPI_SERIES_ID = "CPIAUCSL"

# Date Range for the Last 3 Years
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=3*365)).strftime("%Y-%m-%d")

# Fetch FRED CPI Data
def fetch_fred_data(series_id, start_date, end_date, api_key):
    url = f"{BASE_URL}?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={start_date}&observation_end={end_date}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        observations = data.get("observations", [])
        return observations
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

# Process and Add Percentage Change
def process_cpi_data(observations):
    df = pd.DataFrame(observations)
    df['value'] = df['value'].astype(float)
    df['Percent Change'] = df['value'].pct_change() * 100  # Calculate percent change
    df['Date'] = pd.to_datetime(df['date'])
    df = df[['Date', 'value', 'Percent Change']].rename(columns={'value': 'CPI Index'})
    return df

# Main Process
print("Fetching CPI data...")
cpi_data = fetch_fred_data(CPI_SERIES_ID, start_date, end_date, API_KEY)
if cpi_data:
    processed_data = process_cpi_data(cpi_data)
    processed_data.to_csv("CPI_Data_With_Percent_Change.csv", index=False)
    print("CPI data saved with percent change.")
