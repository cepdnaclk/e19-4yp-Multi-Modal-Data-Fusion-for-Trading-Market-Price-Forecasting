import sys, os
if '__file__' in globals():
    sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from data_prep import load_data
from indicators import add_indicators
from events import (
    find_rsi_events, find_macd_crossovers,
    find_ema_crosses, find_bb_touch,
    find_support_resistance
)

def build_event_dataset(lookback=50, lookahead=5):
    df = add_indicators(load_data())
    features = ['Close','RSI','MACD','MACD_sig','BB_upper','BB_lower','Volume']
    events = find_rsi_events(df)
    for fn in (find_macd_crossovers, find_ema_crosses, find_bb_touch, find_support_resistance):
        events = events.union(fn(df))
    events = events.sort_values().unique()

    X_list, y_list, times = [], [], []
    for t in events:
        pos = np.where(df.index == t)[0]
        if pos.size==0: continue
        idx = pos[0]
        if idx<lookback or idx+lookahead>=len(df): continue
        W = df[features].iloc[idx-lookback:idx].values.astype(np.float32)
        curr = df['Close'].iloc[idx]
        fut = df['Close'].iloc[idx+1:idx+1+lookahead].values[-1]
        label = int(fut>curr)
        X_list.append(W); y_list.append(label); times.append(t)
    return np.array(X_list), np.array(y_list), times

if __name__=='__main__':
    X,y,t = build_event_dataset()
    print(f"Events: {len(t)}, X:{X.shape}, up-rate:{y.mean():.2f}")