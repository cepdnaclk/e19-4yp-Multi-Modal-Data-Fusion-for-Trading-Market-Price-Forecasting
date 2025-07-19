# convert into candle data format
import pandas as pd
import numpy as np

main = pd.read_csv('XAUUSD_30m_from_2018.csv')

# candletype: 0 if close >= open else 1
main['candletype'] = np.where(main['close'] >= main['open'], 0, 1)

# body: absolute difference between open and close
main['candlebody'] = (main['close'] - main['open']).abs()

# uppercandle and lowercandle only if candletype == 0, else 0
main['candleupperwick'] = np.where(main['candletype'] == 0, (main['high'] - main['close']).abs(), 0)
main['candlelowerwick'] = np.where(main['candletype'] == 0, (main['low'] - main['open']).abs(), 0)

main['time'] = pd.to_datetime(main['time'])
df = main[['time', 'close', 'candletype', 'candlebody', 'candleupperwick', 'candlelowerwick', 'tick_volume']].copy()
df = df.rename(columns={'close': 'price'})

# Save the processed DataFrame to a CSV file
df.to_csv('output/processed_XAUUSD_30m.csv', index=False)