# labeling_corrected.py

import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, EMAIndicator, ADXIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from sklearn.preprocessing import MinMaxScaler
from collections import Counter
import joblib

# 1) LOAD RAW DATA
df = pd.read_csv('XAUUSD_30m_from_2018.csv', parse_dates=['time'])

# 2) COMPUTE TECHNICAL INDICATORS
# --- Simple/Exponential Moving Averages ---
df['sma_20'] = SMAIndicator(df['close'], window=20).sma_indicator()
df['sma_50'] = SMAIndicator(df['close'], window=50).sma_indicator()
df['ema_10'] = EMAIndicator(df['close'], window=10).ema_indicator()
df['ema_20'] = EMAIndicator(df['close'], window=20).ema_indicator()

# --- Momentum (RSI) ---
df['rsi'] = RSIIndicator(df['close'], window=14).rsi()

# --- Volatility (Bollinger Bands + ATR) ---
bb = BollingerBands(df['close'], window=20, window_dev=2)
df['bb_upper']  = bb.bollinger_hband()
df['bb_middle'] = bb.bollinger_mavg()
df['bb_lower']  = bb.bollinger_lband()
df['atr']       = AverageTrueRange(df['high'], df['low'], df['close'], window=14).average_true_range()

# --- Trend Strength (ADX) ---
df['adx'] = ADXIndicator(df['high'], df['low'], df['close'], window=14).adx()

# --- MACD (fast=12, slow=26, signal=9) ---
macd = MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
df['macd']        = macd.macd()
df['macd_signal'] = macd.macd_signal()
df['macd_hist']   = macd.macd_diff()

# 3) LABELING PARAMETERS
pip_value          = 0.01     # 1 pip = $0.01 on XAU/USD
spread             = 2 * pip_value
holding_period     = 8        # # of 30m bars (~4h)
# ATR‐based targets; we'll compute inside the function

# 4) REALISTIC TRADER LABEL (EMA crossover + ADX + ATR‐sized TP/SL)
def assign_realistic_label(row, df, idx):
    # need prior bar and enough future bars
    if idx < 1 or idx + holding_period >= len(df):
        return 'neutral'

    entry = row['close']
    atr   = row['atr']
    adx   = row['adx']

    # trend filter
    if adx < 15:
        return 'neutral'

    # dynamic levels
    stop   = 1.0 * atr
    tp_w   = 1.2 * atr
    tp_s   = 1.5 * atr

    prev_e10 = df.at[idx-1, 'ema_10']
    prev_e20 = df.at[idx-1, 'ema_20']
    e10      = row['ema_10']
    e20      = row['ema_20']

    future = df.iloc[idx+1 : idx+1+holding_period]

    # LONG: 10 crosses above 20
    if prev_e10 <= prev_e20 and e10 > e20:
        for _, f in future.iterrows():
            if f['low'] <= entry - stop:
                return 'neutral'
            if f['high'] >= entry + tp_s:
                return 'strong_buy'
            if f['high'] >= entry + tp_w:
                return 'weak_buy'
        return 'neutral'

    # SHORT: 10 crosses below 20
    if prev_e10 >= prev_e20 and e10 < e20:
        for _, f in future.iterrows():
            if f['high'] >= entry + stop:
                return 'neutral'
            if f['low'] <= entry - tp_s:
                return 'strong_sell'
            if f['low'] <= entry - tp_w:
                return 'weak_sell'
        return 'neutral'

    return 'neutral'

# 5) PERFECT HINDSIGHT LABEL (pure future‐move)
def assign_perfect_label(row, df, idx):
    if idx + holding_period >= len(df):
        return 'neutral'

    entry_buy  = row['close'] + spread
    entry_sell = row['close'] - spread
    window     = df.iloc[idx+1 : idx+1+holding_period]

    max_h = window['high'].max()
    min_l = window['low'].min()

    # buy side
    if (max_h - entry_buy) >= 0.01 and (entry_buy - min_l) < 0.01:
        return 'strong_buy'
    if (max_h - entry_buy) >= 0.005 and (entry_buy - min_l) < 0.01:
        return 'weak_buy'

    # sell side
    if (entry_sell - min_l) >= 0.01 and (max_h - entry_sell) < 0.01:
        return 'strong_sell'
    if (entry_sell - min_l) >= 0.005 and (max_h - entry_sell) < 0.01:
        return 'weak_sell'

    return 'neutral'

# 6) APPLY LABELS
df['label']         = [assign_realistic_label(r, df, i) for i,r in df.iterrows()]
df['perfect_label'] = [assign_perfect_label(r, df, i) for i,r in df.iterrows()]

# 7) EXPORT UN‐SCALED CSV FOR VERIFICATION
df.to_csv('forex_data_with_labels_raw.csv', index=False)
print("→ Saved raw labelled data: forex_data_with_labels_raw.csv")

# 8) BUILD SCALE-AND-SEQUENCE DATA FOR LSTM
features = [
    'open','high','low','close','tick_volume',
    'sma_20','sma_50','ema_10','ema_20','rsi',
    'bb_upper','bb_middle','bb_lower',
    'atr','adx','macd','macd_signal','macd_hist'
]

# drop any rows with NaNs
df2 = df.dropna().reset_index(drop=True)

# scale
scaler = MinMaxScaler()
df2[features] = scaler.fit_transform(df2[features])

# window into sequences
seq_len = 20
X, y = [], []
label_map = {'strong_buy':0,'weak_buy':1,'neutral':2,'weak_sell':3,'strong_sell':4}

for i in range(len(df2) - seq_len):
    X.append(df2[features].iloc[i:i+seq_len].values)
    y.append(label_map[df2.at[i+seq_len, 'label']])

X = np.array(X)
y = np.array(y)

# train/test split
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# save
np.save('X_train.npy', X_train)
np.save('X_test.npy',  X_test)
np.save('y_train.npy', y_train)
np.save('y_test.npy',  y_test)
joblib.dump(scaler, 'scaler.pkl')

print(f"→ Sequences saved. X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
print(f"Realistic vs. Perfect match: { (df2['label']==df2['perfect_label']).mean()*100 :.2f}%")
print("Label counts:", Counter(df2['label']), Counter(df2['perfect_label']))
