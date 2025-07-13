# src/dataset.py

import sys, os
# Ensure local modules are importable
if '__file__' in globals():
    sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from data_prep import load_data
from indicators import add_indicators

def build_sequences(df, features, target_col='Close', window=50):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df[features])

    X, y = [], []
    for i in range(window, len(scaled) - 1):
        X.append(scaled[i-window:i])
        cur = scaled[i, features.index(target_col)]
        nxt = scaled[i+1, features.index(target_col)]
        y.append(int(nxt > cur))

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int32), scaler

if __name__ == '__main__':
    df = load_data()                     # no arguments
    df = add_indicators(df)
    feats = ['Close','RSI','MACD','MACD_sig','BB_upper','BB_lower','Volume']
    X, y, scaler = build_sequences(df, feats, window=50)
    print('X shape:', X.shape, 'y shape:', y.shape)
