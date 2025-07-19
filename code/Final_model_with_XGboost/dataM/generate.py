import pandas as pd
import numpy as np
from datetime import datetime

# Load gold price data
gold_df = pd.read_csv("XAUUSD_MN1.csv")
gold_df['date'] = pd.to_datetime(gold_df['time']).dt.to_period('M').dt.to_timestamp()
gold_df = gold_df[['date', 'close']]
gold_df.rename(columns={'close': 'price'}, inplace=True)

# Define macroeconomic file paths
macro_files = {
    'CPI': "CPI.csv",
    'GDP': "GDP.csv",
    'I_R': "Interest Rate.csv",
    'NFP': "NFP.csv",
    'PCE': "PCE.csv",
    'PPI': "PPI.csv"
}

# Function to normalize NFP values like '151K', '1.2M'
def normalize_nfp(value):
    if isinstance(value, str):
        value = value.replace(',', '').strip()
        if value.endswith('K'):
            return float(value[:-1]) * 1000
        elif value.endswith('M'):
            return float(value[:-1]) * 1_000_000
        else:
            try:
                return float(value)
            except:
                return np.nan
    return value

# Load and process each macro file
macro_data = {}
for label, file_path in macro_files.items():
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])  # drop rows with invalid dates
    if label == 'NFP':
        df['Actual'] = df['Actual'].apply(normalize_nfp)
    else:
        df['Actual'] = pd.to_numeric(df['Actual'], errors='coerce')
    df = df[['date', 'Actual']].sort_values('date')
    macro_data[label] = df

# Function to get the latest available macro value for a month
def map_macro_to_date(target_date, macro_df):
    target_month = target_date.to_period('M')
    same_month = macro_df[macro_df['date'].dt.to_period('M') == target_month]
    if not same_month.empty:
        return same_month.iloc[-1]['Actual']
    else:
        prev = macro_df[macro_df['date'] < target_date]
        if not prev.empty:
            return prev.iloc[-1]['Actual']
    return np.nan

# Map each macro to the gold price dataframe
for label, macro_df in macro_data.items():
    gold_df[label] = gold_df['date'].apply(lambda x: map_macro_to_date(x, macro_df))

# Final ordering of columns
final_df = gold_df[['date', 'CPI', 'GDP', 'I_R', 'NFP', 'PCE', 'PPI', 'price']]

# Optional: save to CSV
final_df.to_csv("monthly_macro_gold_dataset.csv", index=False)

print("✅ Dataset created successfully as 'monthly_macro_gold_dataset.csv'")
