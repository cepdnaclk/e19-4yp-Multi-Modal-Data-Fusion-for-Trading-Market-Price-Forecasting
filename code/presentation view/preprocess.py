import pandas as pd
from data_preparation import excel_serial_to_datetime_str
import datetime

'''
  1. Missing data handling - Interpolation - Forward filling
  2. Normalization and scaling
   3. Outlier detection
  5. Feature Engineering
  6. Correlation & Feature Selection
  '''
  
# Load forex data
forex = pd.read_csv('./Data/XAUUSD_1M_markettrend.csv', parse_dates=['time'])

'''4. Time series data preprocessing - Date & Time Conversion'''
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


def merge_macro_to_forex(forex_df, macro_df, factor_name, forex_timeframe='1H'):
    macro_df['datetime'] = macro_df.apply(parse_macro_datetime, axis=1)
    forex_df = forex_df.sort_values('time')
    macro_df = macro_df.sort_values('datetime')

  '''- Resampling - to a common frequency'''
    # Handle special timeframe flooring inside the function
    def floor_times(series, timeframe):
        if timeframe == '1W':
            return series.dt.to_period('W').dt.start_time
        elif timeframe == '1M':
            return series.dt.to_period('M').dt.start_time
        else:
            return series.dt.floor(timeframe)

    # FLOOR times according to timeframe with special handling
    forex_df['time_floor'] = floor_times(forex_df['time'], forex_timeframe)
    macro_df['datetime_floor'] = floor_times(macro_df['datetime'], forex_timeframe)
    
    # Use floored times for merge_asof
    merged = pd.merge_asof(macro_df, forex_df,
                           left_on='datetime_floor', right_on='time_floor',
                           direction='forward')

    # Keep only needed macro columns with datetime_floor renamed to 'time'
    macro_cols = ['datetime_floor', 'Actual', 'Forecast', 'Previous']
    macro_renamed = merged[macro_cols].rename(columns={
        'datetime_floor': 'time',
        'Actual': f'{factor_name}_Actual',
        'Forecast': f'{factor_name}_Forecast',
        'Previous': f'{factor_name}_Previous'
    })

    # Merge back to full forex on floored time
    result = pd.merge(forex_df, macro_renamed, on='time', how='left')

    # Forward fill macro columns
    macro_fill_cols = [f'{factor_name}_Actual', f'{factor_name}_Forecast', f'{factor_name}_Previous']
    result[macro_fill_cols] = result[macro_fill_cols].fillna(method='ffill')

    # Drop helper column to keep original forex time
    result.drop(columns=['time_floor'], inplace=True, errors='ignore')

    return result


# Load CPI and GDP data
cpi = pd.read_excel('./data/CPI.xlsx')
gdp = pd.read_excel('./data/GDP.xlsx')
# Load the new macroeconomic data
interest_rate = pd.read_excel('./data/Interest_Rate.xlsx')
nfp = pd.read_excel('./data/NFP.xlsx')
pce = pd.read_excel('./data/PCE.xlsx')
ppi = pd.read_excel('./data/PPI.xlsx')

forex_timeframe = '1M'  # Change to your data timeframe

# Merge the new macroeconomic data with the forex data
forex_with_cpi = merge_macro_to_forex(forex, cpi, 'CPI',forex_timeframe)
forex_with_gdp = merge_macro_to_forex(forex_with_cpi, gdp, 'GDP',forex_timeframe)
forex_with_interest_rate = merge_macro_to_forex(forex_with_gdp, interest_rate, 'Interest_Rate',forex_timeframe)
forex_with_nfp = merge_macro_to_forex(forex_with_interest_rate, nfp, 'NFP',forex_timeframe)
forex_with_pce = merge_macro_to_forex(forex_with_nfp, pce, 'PCE',forex_timeframe)
forex_with_ppi = merge_macro_to_forex(forex_with_pce, ppi, 'PPI',forex_timeframe)

# Save merged data to Excel
output_file = './data/forex_with_all_macros_1M.xlsx'
forex_with_ppi.dropna(inplace=True)
forex_with_ppi.to_excel(output_file, index=False)

print(f'Merged data saved to {output_file}')

# For human-readable time format
human_df = forex_with_ppi
human_df = human_df.reset_index()
human_df['time'] = excel_serial_to_datetime_str(human_df['time'])
human_df.dropna(inplace=True)

# Save the human-readable time version
human_df.to_excel('./data/human_readable_time_all_macros_1M.xlsx', index=False)
print("Saved merged data to human_readable_time_all_macros.xlsx")
