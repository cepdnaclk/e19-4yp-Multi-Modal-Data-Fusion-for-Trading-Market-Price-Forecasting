# src/visualize.py

import sys, os
# Enable imports from src/
if '__file__' in globals():
    sys.path.insert(0, os.path.dirname(__file__))

import plotly.graph_objects as go
from evaluate import backtest

def plot_signals(output_html: str = 'signals.html'):
    dates, signals, price, cumret = backtest()

    fig = go.Figure(data=[
        go.Candlestick(
            x=dates,
            open=price, high=price*1.001, low=price*0.999, close=price,
            name='Price'
        )
    ])

    # markers: buy when signal=1, sell when signal=0
    buy_idxs = [i for i,s in enumerate(signals) if s==1]
    sell_idxs = [i for i,s in enumerate(signals) if s==0]

    fig.add_trace(go.Scatter(
        x=[dates[i] for i in buy_idxs],
        y=[price[i] for i in buy_idxs],
        mode='markers', marker_symbol='triangle-up', marker_size=10,
        name='BUY'
    ))
    fig.add_trace(go.Scatter(
        x=[dates[i] for i in sell_idxs],
        y=[price[i] for i in sell_idxs],
        mode='markers', marker_symbol='triangle-down', marker_size=10,
        name='SELL'
    ))

    fig.update_layout(
        title='XAUUSD 30m Forecast Signals',
        xaxis_rangeslider_visible=False
    )

    # ensure output directory exists
    out_path = os.path.abspath(output_html)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.write_html(out_path)
    print(f"Visualization saved to {out_path}")

if __name__ == '__main__':
    # Save the chart as signals.html in project root
    plot_signals('signals.html')
