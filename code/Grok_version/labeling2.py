import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, MACD, EMAIndicator, ADXIndicator
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from sklearn.preprocessing import MinMaxScaler
from collections import Counter

# Load the CSV file
df = pd.read_csv('./Data/XAUUSD_30m_from_2018.csv', parse_dates=['time'])

# Compute Technical Indicators
df['sma_20'] = SMAIndicator(df['close'], window=20).sma_indicator()
df['sma_50'] = SMAIndicator(df['close'], window=50).sma_indicator()
df['rsi'] = RSIIndicator(df['close'], window=14).rsi()

bb = BollingerBands(df['close'], window=20, window_dev=2)
df['bb_upper']  = bb.bollinger_hband()
df['bb_lower']  = bb.bollinger_lband()
df['bb_middle'] = bb.bollinger_mavg()

macd = MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
df['macd']        = macd.macd()
df['macd_signal'] = macd.macd_signal()
df['macd_hist']   = macd.macd_diff()

df['atr'] = AverageTrueRange(df['high'], df['low'], df['close'], window=14).average_true_range()

# ---- New: Faster EMAs & ADX for trend filtering ----
df['ema_10'] = EMAIndicator(df['close'], window=10).ema_indicator()
df['ema_20'] = EMAIndicator(df['close'], window=20).ema_indicator()
df['adx']    = ADXIndicator(df['high'], df['low'], df['close'], window=14).adx()

# Define Parameters (unchanged)
pip_value          = 0.01  # Adjust for XAU/USD
spread             = 2 * pip_value
take_profit_strong = 10 * pip_value
take_profit_weak   = 5  * pip_value
stop_loss          = 8  * pip_value
holding_period     = 8    # 4 hours = 8 candles of 30 minutes

# ---- Updated Realistic Trader Labeling ----
def assign_realistic_label(row, df, idx):
    # ensure we have both a prior bar and future bars
    if idx < 1 or idx + holding_period >= len(df):
        return 'neutral'
    
    close       = row['close']
    atr         = row['atr']
    adx         = row['adx']
    ema10       = row['ema_10']
    ema20       = row['ema_20']
    prev_ema10  = df['ema_10'].iat[idx-1]
    prev_ema20  = df['ema_20'].iat[idx-1]
    
    # only enter trades in a trending market
    if adx < 15:
        return 'neutral'
    
    # dynamic risk/reward via ATR
    stop_level   = atr
    tp_strong_atr = 2.0 * atr
    tp_weak_atr   = 1.5 * atr
    
    # simulate candle-by-candle to see which level hits first
    future = df.iloc[idx+1 : idx+holding_period+1]
    entry  = close

    # LONG: EMA10 crosses above EMA20
    if prev_ema10 <= prev_ema20 and ema10 > ema20:
        for _, f in future.iterrows():
            if f['low'] <= entry - stop_level:
                return 'neutral'
            if f['high'] >= entry + tp_strong_atr:
                return 'strong_buy'
            if f['high'] >= entry + tp_weak_atr:
                return 'weak_buy'
        return 'neutral'
    
    # SHORT: EMA10 crosses below EMA20
    if prev_ema10 >= prev_ema20 and ema10 < ema20:
        for _, f in future.iterrows():
            if f['high'] >= entry + stop_level:
                return 'neutral'
            if f['low'] <= entry - tp_strong_atr:
                return 'strong_sell'
            if f['low'] <= entry - tp_weak_atr:
                return 'weak_sell'
        return 'neutral'
    
    return 'neutral'

# Perfect Hindsight Labeling (unchanged)
def assign_perfect_label(row, df, idx):
    if idx + holding_period >= len(df):
        return 'neutral'
    
    close         = row['close']
    future_prices = df.iloc[idx:idx+holding_period+1][['high','low']].values
    max_high      = np.max(future_prices[:,0])
    min_low       = np.min(future_prices[:,1])
    
    # buy side
    buy_entry  = close + spread
    buy_profit = max_high - buy_entry
    buy_loss   = buy_entry - min_low
    if buy_profit >= take_profit_strong and buy_loss < stop_loss:
        return 'strong_buy'
    if buy_profit >= take_profit_weak   and buy_loss < stop_loss:
        return 'weak_buy'
    
    # sell side
    sell_entry  = close - spread
    sell_profit = sell_entry - min_low
    sell_loss   = max_high - sell_entry
    if sell_profit >= take_profit_strong and sell_loss < stop_loss:
        return 'strong_sell'
    if sell_profit >= take_profit_weak   and sell_loss < stop_loss:
        return 'weak_sell'
    
    return 'neutral'

# Apply both labeling functions
df['label']         = [assign_realistic_label(r, df, i) for i,r in df.iterrows()]
df['perfect_label'] = [assign_perfect_label(r, df, i) for i,r in df.iterrows()]

# Compare and report
df['match'] = df['label'] == df['perfect_label']
accuracy   = df['match'].mean() * 100
print(f"Realistic labels match perfect labels: {accuracy:.2f}%")
print("Realistic distribution:", Counter(df['label']))
print("Perfect distribution:   ", Counter(df['perfect_label']))

# Data Preprocessing for LSTM
features = ['open','high','low','close','tick_volume',
            'sma_20','sma_50','rsi','bb_upper','bb_lower','bb_middle',
            'macd','macd_signal','macd_hist','atr']
df = df.dropna()

scaler = MinMaxScaler()
df[features] = scaler.fit_transform(df[features])

sequence_length = 20
X, y = [], []
label_map = {'strong_buy':0,'weak_buy':1,'neutral':2,'weak_sell':3,'strong_sell':4}

for i in range(len(df) - sequence_length):
    X.append(df[features].iloc[i:i+sequence_length].values)
    y.append(label_map[df['label'].iloc[i+sequence_length]])

X = np.array(X)
y = np.array(y)

# Train-test split
train_size   = int(0.8 * len(X))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Save outputs
np.save('X_train_dual.npy', X_train)
np.save('X_test_dual.npy',  X_test)
np.save('y_train_dual.npy', y_train)
np.save('y_test_dual.npy',  y_test)

import joblib
joblib.dump(scaler, 'scaler_dual.pkl')
df.to_csv('forex_data_with_labels2.csv', index=False)

print("Preprocessed data saved. X_train shape:", X_train.shape, "y_train shape:", y_train.shape)
