import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from technical_indicators import *


def load_forex_data(path):
    df = pd.read_csv(path)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)
    return df

def calculate_technical_indicators(df):
    df['MA_50'] = moving_average(df['close'], 50)
    df['MA_200'] = moving_average(df['close'], 200)
    df['MACD'] = macd(df['close'])
    # df['Momentum_4'] = momentum(df['close'], 4)
    # df['ROC_2'] = rate_of_change(df['close'], 2)
    df['RSI_14'] = relative_strength_index(df['close'], 14)
    df['BB_upper'], df['BB_lower'] = bollinger_bands(df['close'])
    # df['CCI_20'] = commodity_channel_index(df)
    df.dropna(inplace=True)
    return df

# remove other indicators(RSI,MA50,200)

def label_data(df, threshold=0.0005):
    df['close_next'] = df['close'].shift(-1)
    df['price_diff'] = df['close_next'] - df['close']

    def label_direction(diff):
        if diff > threshold:
            return 2  # increase
        elif diff < -threshold:
            return 1  # decrease
        else:
            return 0  # no_action

    df['label'] = df['price_diff'].apply(label_direction)
    df.dropna(inplace=True)
    return df

def create_sequences(df, features, label_col, time_steps=30):
    X, y = [], []
    for i in range(len(df) - time_steps):
        X.append(df[features].iloc[i:i+time_steps].values)
        y.append(df[label_col].iloc[i+time_steps])
    return np.array(X), np.array(y)

def scale_features(X_train, X_test):
    num_features = X_train.shape[2]
    scaler = RobustScaler()

    X_train_2d = X_train.reshape(-1, num_features)
    X_test_2d = X_test.reshape(-1, num_features)

    scaler.fit(X_train_2d)

    X_train_scaled = scaler.transform(X_train_2d).reshape(X_train.shape)
    X_test_scaled = scaler.transform(X_test_2d).reshape(X_test.shape)

    return X_train_scaled, X_test_scaled

# def merge_cpi_with_forex(forex_df, cpi_path):
#     cpi_df = pd.read_excel(cpi_path)
    
#     # Extract the date part before any parenthesis or extra text
#     # For example: "Apr 10, 2025 (Mar)" --> "Apr 10, 2025"
#     cpi_df['Release Date'] = cpi_df['Release Date'].str.extract(r'([A-Za-z]{3,9}\s\d{1,2},\s\d{4})')[0]
    
#     # Now parse with to_datetime without format - let pandas infer format
#     cpi_df['Release Date'] = pd.to_datetime(cpi_df['Release Date'], errors='coerce')
    
#     # Drop rows where parsing failed (NaT)
#     cpi_df = cpi_df.dropna(subset=['Release Date'])
    
#     cpi_df.sort_values('Release Date', inplace=True)
#     cpi_df.set_index('Release Date', inplace=True)
    
#     # Keep only needed columns
#     cpi_df = cpi_df[['Actual', 'Forecast', 'Previous']]
    
#     # Forward-fill CPI values to daily frequency to match forex 30min data
#     cpi_df = cpi_df.resample('D').ffill()
    
#     # Join on the floored date part of forex_df index
#     merged = forex_df.copy()
#     merged = merged.join(cpi_df, on=merged.index.floor('D'))
    
#     merged.dropna(inplace=True)
    
#     return merged

# def merge_macro_with_forex(forex_df, macro_df):
#     """
#     Merge combined macroeconomic DataFrame with forex_df on floored date.

#     Assumes:
#     - macro_df has a datetime index at daily frequency
#     - forex_df has a datetime index at 30-min frequency

#     Returns merged DataFrame with macro data joined.
#     """
#     # Ensure macro_df index is datetime and sorted
#     macro_df = macro_df.sort_index()
#     macro_df.index = pd.to_datetime(macro_df.index)

#     # Join on floored datetime index (floor to day)
#     merged = forex_df.copy()
#     merged = merged.join(macro_df, on=merged.index.floor('D'))

#     # Drop rows with missing macro data
#     merged.dropna(inplace=True)

#     return merged

def load_macro_data_with_prefix(path, prefix):
    df = pd.read_excel(path)

    # Extract date part from 'Release Date' column
    df['Release Date'] = df['Release Date'].str.extract(r'([A-Za-z]{3,9}\s\d{1,2},\s\d{4})')[0]

    # Combine 'Release Date' and 'Time' columns into one datetime string
    df['Release DateTime'] = df['Release Date'] + ' ' + df['Time'].astype(str)

    # Parse combined datetime string
    df['Release DateTime'] = pd.to_datetime(df['Release DateTime'], errors='coerce')

    # Drop rows where parsing failed
    df = df.dropna(subset=['Release DateTime'])

    # Sort by the new datetime index
    df = df.sort_values('Release DateTime')

    # Keep only relevant columns and rename
    df = df[['Release DateTime', 'Actual', 'Forecast', 'Previous']]
    df = df.rename(columns={
        'Actual': f'{prefix}_Actual',
        'Forecast': f'{prefix}_Forecast',
        'Previous': f'{prefix}_Previous'
    })

    # Set the combined datetime as index
    df.set_index('Release DateTime', inplace=True)

    # Now resample with 30-min frequency to match forex data time intervals
    # Forward fill missing values to cover all forex timestamps
    df = df.resample('30T').ffill()

    return df


def merge_multiple_macros(forex_df, macro_dfs):
    merged = forex_df.copy()

    for macro_df in macro_dfs:
        merged = merged.join(macro_df, how='left')

    merged = merged.dropna()
    return merged


def excel_serial_to_datetime_str(series):
    import pandas as pd

    if pd.api.types.is_numeric_dtype(series):
        # Convert Excel serial to datetime first
        dt = pd.to_datetime('1899-12-30') + pd.to_timedelta(series, unit='D')
    elif pd.api.types.is_datetime64_any_dtype(series):
        # Already datetime, just use it as is
        dt = series
    else:
        raise TypeError("Input series must be either Excel serial numbers or datetime64")

    # Format datetime to string like 'YYYY/MM/DD 12:30pm'
    return dt.dt.strftime('%Y/%m/%d %I:%M%p').str.lower()




