import pandas as pd
from data_preparation import excel_serial_to_datetime_str
# Load forex data
forex = pd.read_csv('./data/XAUUSD_30m_from_2018.csv', parse_dates=['time'])

def parse_macro_datetime(row):
    date_str = row['Release Date'].split(' (')[0]
    date = pd.to_datetime(date_str).date()
    
    t = row['Time']
    # If t is a string, parse it to datetime.time first
    if isinstance(t, str):
        t = pd.to_datetime(t).time()
    
    time_delta = pd.Timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    
    return pd.Timestamp(date) + time_delta


def merge_macro_to_forex(forex_df, macro_df, factor_name):
    macro_df['datetime'] = macro_df.apply(parse_macro_datetime, axis=1)
    forex_df = forex_df.sort_values('time')
    macro_df = macro_df.sort_values('datetime')
    merged = pd.merge_asof(macro_df, forex_df, left_on='datetime', right_on='time', direction='forward')
    
    macro_cols = ['datetime', 'Actual', 'Forecast', 'Previous']
    macro_renamed = merged[macro_cols].rename(columns={
        'Actual': f'{factor_name}_Actual',
        'Forecast': f'{factor_name}_Forecast',
        'Previous': f'{factor_name}_Previous',
        'datetime': 'time'
    })
    
    # Merge into forex
    result = pd.merge(forex_df, macro_renamed, on='time', how='left')
    
    # Forward fill macroeconomic columns to persist values until next update
    macro_fill_cols = [f'{factor_name}_Actual', f'{factor_name}_Forecast', f'{factor_name}_Previous']
    result[macro_fill_cols] = result[macro_fill_cols].fillna(method='ffill')
    
    return result


# Load CPI and GDP data
cpi = pd.read_excel('./data/CPI.xlsx')
gdp = pd.read_excel('./data/GDP.xlsx')

# Merge macroeconomic data
forex_with_cpi = merge_macro_to_forex(forex, cpi, 'CPI')
forex_with_all = merge_macro_to_forex(forex_with_cpi, gdp, 'GDP')

# Save to Excel
output_file = './data/forex_with_macro.xlsx'
forex_with_all.dropna(inplace=True)
forex_with_all.to_excel(output_file, index=False)

print(f'Merged data saved to {output_file}')

human_df= forex_with_all
human_df = human_df.reset_index()
human_df['time'] = excel_serial_to_datetime_str(human_df['time'])
human_df.dropna(inplace=True)

# Save to Excel with formatted time strings
human_df.to_excel('./data/human_readable_time.xlsx', index=False)
print("Saved merged data to human_readable_time.xlsx")
