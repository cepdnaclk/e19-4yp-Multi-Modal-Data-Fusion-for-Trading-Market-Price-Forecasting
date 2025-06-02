import pandas as pd
from technical_indicators import *

# Load Forex price data
forex_path = 'XAUUSD_30m_from_2018.csv'
forex_df = pd.read_csv(forex_path)

# Show basic info and first rows
print(forex_df.info())
print(forex_df.head())

forex_df['time'] = pd.to_datetime(forex_df['time'])
forex_df.set_index('time', inplace=True)

print(forex_df.head())

# Load your data here...

# Calculate indicators
forex_df['MA_10'] = moving_average(forex_df['close'], 10)
forex_df['MACD'] = macd(forex_df['close'])
forex_df['Momentum_4'] = momentum(forex_df['close'], 4)
forex_df['ROC_2'] = rate_of_change(forex_df['close'], 2)
forex_df['RSI_14'] = relative_strength_index(forex_df['close'], 14)
forex_df['BB_upper'], forex_df['BB_lower'] = bollinger_bands(forex_df['close'])
forex_df['CCI_20'] = commodity_channel_index(forex_df)

# Continue with your processing...
forex_df.dropna(inplace=True)

print(forex_df.tail())
