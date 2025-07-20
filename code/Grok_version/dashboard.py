# dashboard.py
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def downsample_to_pixels(df: pd.DataFrame, pixel_width: int = 3000) -> pd.DataFrame:
    """
    Aggressively downsample df so that you end up with at most `pixel_width`
    rows, picking evenly-spaced indices so the chart stays smooth.
    """
    n = len(df)
    if n <= pixel_width:
        return df
    idx = np.linspace(0, n - 1, pixel_width, dtype=int)
    return df.iloc[idx]

def main():
    # 1) Load & parse full data
    df = pd.read_csv('forex_data_with_labels.csv', parse_dates=['time'])
    df.sort_values('time', inplace=True)
    df.set_index('time', inplace=True)

    # 2) Compute y-axis limits from the full data
    y_min, y_max = df['low'].min(), df['high'].max()

    # 3) Downsample for plotting speed
    df_ds = downsample_to_pixels(df, pixel_width=3000)

    # 4) Build Plotly figure
    fig = go.Figure()

    # 4a) Candlesticks (SVG)
    fig.add_trace(go.Candlestick(
        x=df_ds.index,
        open=df_ds['open'],
        high=df_ds['high'],
        low =df_ds['low'],
        close=df_ds['close'],
        increasing_line_color='green',
        decreasing_line_color='red',
        name='Price',
        showlegend=False
    ))

    # 4b) Close-price line (WebGL)
    fig.add_trace(go.Scattergl(
        x=df_ds.index,
        y=df_ds['close'],
        mode='lines',
        line=dict(color='blue', width=1),
        name='Close'
    ))

    # 4c) Perfect-label ▲/▼ markers (WebGL)
    buys  = df_ds[df_ds['perfect_label']=='strong_buy']
    sells = df_ds[df_ds['perfect_label']=='strong_sell']
    fig.add_trace(go.Scattergl(
        x=buys.index, y=buys['low'],
        mode='markers',
        marker_symbol='triangle-up',
        marker_color='green',
        marker_size=10,
        name='Buy'
    ))
    fig.add_trace(go.Scattergl(
        x=sells.index, y=sells['high'],
        mode='markers',
        marker_symbol='triangle-down',
        marker_color='red',
        marker_size=10,
        name='Sell'
    ))

    # 5) Layout & interactivity
    fig.update_layout(
        title='XAU/USD 30m — Downsampled Price with Perfect-Label Signals',
        template='plotly_white',
        xaxis_title='Time',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        dragmode='zoom',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )

    # 6) Force full-data y-axis range
    fig.update_yaxes(range=[y_min, y_max])

    # 7) Mouse-wheel zoom
    fig.show(config={'scrollZoom': True})

if __name__ == '__main__':
    main()
