# src/visualize_events.py

import sys, os
from pathlib import Path
if '__file__' in globals():
    sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tensorflow.keras.models import load_model

from data_prep import load_data
from indicators import add_indicators
from events import (
    find_rsi_events,
    find_macd_crossovers,
    find_ema_crosses,
    find_bb_touch,
    find_support_resistance
)
from model_events import sum_time
from dataset_events import build_event_dataset

# 1) Load and indicator-engineer full price series
df = add_indicators(load_data())

# 2) Build event dataset and model predictions
X_events, y_events, event_times = build_event_dataset()
models_dir = Path(__file__).resolve().parent.parent / 'models_events'
event_model = load_model(
    models_dir / 'event_model.h5',
    custom_objects={'sum_time': sum_time}
)
probs = event_model.predict(X_events).ravel()
signals = probs > 0.5
buy_times = [t for t, s in zip(event_times, signals) if s]
sell_times = [t for t, s in zip(event_times, signals) if not s]

# 3) Prepare indicator series
ema_fast = df['Close'].ewm(span=12, adjust=False).mean()
ema_slow = df['Close'].ewm(span=26, adjust=False).mean()
bb_upper = df['BB_upper']
bb_lower = df['BB_lower']
rsi_line = df['RSI']
macd_line = df['MACD']
macd_sig  = df['MACD_sig']

# 4) Build 3-row subplot figure
fig = make_subplots(
    rows=3, cols=1, shared_xaxes=True,
    row_heights=[0.5, 0.25, 0.25], vertical_spacing=0.03
)

# --- Row 1: Price + EMAs + BB + buy/sell ---
fig.add_trace(go.Scatter(
    x=df.index, y=df['Close'],
    mode='lines', name='Price'
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=df.index, y=ema_fast,
    mode='lines', name='EMA Fast'
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=df.index, y=ema_slow,
    mode='lines', name='EMA Slow'
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=df.index, y=bb_upper,
    mode='lines', name='BB Upper',
    line={'dash':'dash'}
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=df.index, y=bb_lower,
    mode='lines', name='BB Lower',
    line={'dash':'dash'}
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=buy_times, y=df.loc[buy_times,'Close'],
    mode='markers',
    marker_symbol='triangle-up', marker_color='green',
    name='Buy Signal'
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=sell_times, y=df.loc[sell_times,'Close'],
    mode='markers',
    marker_symbol='triangle-down', marker_color='red',
    name='Sell Signal'
), row=1, col=1)

# --- Row 2: RSI ---
fig.add_trace(go.Scatter(
    x=df.index, y=rsi_line,
    mode='lines', name='RSI'
), row=2, col=1)
fig.add_hline(y=70, line_dash='dash', annotation_text='Overbought', row=2, col=1)
fig.add_hline(y=30, line_dash='dash', annotation_text='Oversold', row=2, col=1)

# --- Row 3: MACD ---
fig.add_trace(go.Scatter(
    x=df.index, y=macd_line,
    mode='lines', name='MACD'
), row=3, col=1)
fig.add_trace(go.Scatter(
    x=df.index, y=macd_sig,
    mode='lines', name='MACD Signal'
), row=3, col=1)

fig.update_layout(
    title='Event-Based Signals & Indicators',
    xaxis_rangeslider_visible=False,
    height=900
)

# 5) Save HTML
out_html = Path(__file__).resolve().parent.parent / 'outputs' / 'event_dashboard.html'
out_html.parent.mkdir(parents=True, exist_ok=True)
fig.write_html(out_html)
print(f"Saved enhanced dashboard to {out_html}")
