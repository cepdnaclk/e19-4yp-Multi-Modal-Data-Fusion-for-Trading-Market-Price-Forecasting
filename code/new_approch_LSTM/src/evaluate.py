# src/evaluate.py

import sys, os
# Enable imports from src/
if '__file__' in globals():
    sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

from data_prep import load_data
from indicators import add_indicators
from dataset import build_sequences
from model import sum_time  # custom function for Lambda layer

def backtest():
    # Load data and compute indicators
    df = load_data()
    df = add_indicators(df)

    # Features and window
    feats = ['Close', 'RSI', 'MACD', 'MACD_sig', 'BB_upper', 'BB_lower', 'Volume']
    window = 50
    X_all, y_all, _ = build_sequences(df, feats, window=window)

    # Load model with custom_objects
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'fx_lstm_attn.h5'))
    model = load_model(model_path, custom_objects={'sum_time': sum_time})

    # Generate signals (binary)
    preds = model.predict(X_all).ravel()
    signals = (preds > 0.5).astype(int)

    # Compute simple returns: align lengths
    price = df['Close'].values[window:-1]       # len = N_window-1
    signals = signals[:-1]                      # drop last signal to match returns length
    returns = np.where(signals == 1,
                       np.diff(price) / price[:-1],
                       -np.diff(price) / price[:-1])

    # Cumulative return
    cumret = np.cumprod(1 + returns) - 1
    print('Final cumulative return:', cumret[-1])

    # Return aligned index, signals, price, and cumret
    dates = df.index[window+1:-1]               # align with returns
    return dates, signals, price[:-1], cumret

if __name__ == '__main__':
    backtest()
