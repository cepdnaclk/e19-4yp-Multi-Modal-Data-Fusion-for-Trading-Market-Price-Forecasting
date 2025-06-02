import pandas as pd
from data_preparation import excel_serial_to_datetime_str
import datetime

# Load forex data
forex = pd.read_csv('./Data/XAUUSD_1H_markettrend.csv', parse_dates=['time'])

# Updated function to parse Release Date and Time
def parse_macro_datetime(row):
    release_date = row['Release Date']
    
    # Check if 'Release Date' is a string
    if isinstance(release_date, str):
        # Extract the date part from the string (e.g., "May 02, 2025 (Apr)")
        date_str = release_date.split(' (')[0]
        date = pd.to_datetime(date_str).date()
    elif isinstance(release_date, pd.Timestamp) or isinstance(release_date, datetime.datetime):
        # If 'Release Date' is already a Timestamp or datetime.datetime, use it directly
        date = release_date.date()
    else:
        raise TypeError(f"Unknown type for 'Release Date': {type(release_date)}")
    
    t = row['Time']
    # If 'Time' is a string, parse it to datetime.time first
    if isinstance(t, str):
        t = pd.to_datetime(t).time()
    
    time_delta = pd.Timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    
    # Combine date and time
    return pd.Timestamp(date) + time_delta


# Function to merge macroeconomic data with forex data
def merge_macro_to_forex(forex_df, macro_df, factor_name):
    macro_df['datetime'] = macro_df.apply(parse_macro_datetime, axis=1)
    forex_df = forex_df.sort_values('time')
    macro_df = macro_df.sort_values('datetime')
    
    # Use merge_asof to align macro data with forex data
    merged = pd.merge_asof(macro_df, forex_df, left_on='datetime', right_on='time', direction='forward')
    
    # Rename macro columns
    macro_cols = ['datetime', 'Actual', 'Forecast', 'Previous']
    macro_renamed = merged[macro_cols].rename(columns={
        'Actual': f'{factor_name}_Actual',
        'Forecast': f'{factor_name}_Forecast',
        'Previous': f'{factor_name}_Previous',
        'datetime': 'time'
    })
    
    # Merge into forex data
    result = pd.merge(forex_df, macro_renamed, on='time', how='left')
    
    # Forward fill missing macroeconomic columns
    macro_fill_cols = [f'{factor_name}_Actual', f'{factor_name}_Forecast', f'{factor_name}_Previous']
    result[macro_fill_cols] = result[macro_fill_cols].fillna(method='ffill')
    
    return result

# Load CPI and GDP data
cpi = pd.read_excel('./data/CPI.xlsx')
gdp = pd.read_excel('./data/GDP.xlsx')
# Load the new macroeconomic data
interest_rate = pd.read_excel('./data/Interest_Rate.xlsx')
nfp = pd.read_excel('./data/NFP.xlsx')
pce = pd.read_excel('./data/PCE.xlsx')
ppi = pd.read_excel('./data/PPI.xlsx')

# Merge the new macroeconomic data with the forex data
forex_with_cpi = merge_macro_to_forex(forex, cpi, 'CPI')
forex_with_gdp = merge_macro_to_forex(forex_with_cpi, gdp, 'GDP')
forex_with_interest_rate = merge_macro_to_forex(forex_with_gdp, interest_rate, 'Interest_Rate')
# forex_with_nfp = merge_macro_to_forex(forex_with_interest_rate, nfp, 'NFP')
forex_with_pce = merge_macro_to_forex(forex_with_interest_rate, pce, 'PCE')
forex_with_ppi = merge_macro_to_forex(forex_with_pce, ppi, 'PPI')

# Save merged data to Excel
output_file = './data/forex_with_all_macros_1D.xlsx'
forex_with_ppi.dropna(inplace=True)
forex_with_ppi.to_excel(output_file, index=False)

print(f'Merged data saved to {output_file}')

# For human-readable time format
human_df = forex_with_ppi
human_df = human_df.reset_index()
human_df['time'] = excel_serial_to_datetime_str(human_df['time'])
human_df.dropna(inplace=True)

# Save the human-readable time version
human_df.to_excel('./data/human_readable_time_all_macros_1H.xlsx', index=False)
print("Saved merged data to human_readable_time_all_macros.xlsx")
