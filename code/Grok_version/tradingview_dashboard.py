import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler

# Load the labeled dataset
df = pd.read_csv('forex_data_with_labels.csv', parse_dates=['time'])

# Remove the 1000-candle limit to show full dataset
# df = df.iloc[-1000:]  # Commented out to allow full data

# Handle NaN values
df = df.dropna(subset=['rsi', 'sma_20', 'sma_50', 'open', 'high', 'low', 'close', 'bb_upper', 'bb_lower', 'bb_middle', 'macd', 'macd_signal', 'macd_hist', 'atr'])

# Load the scaler to inverse-transform all scaled features
try:
    scaler = joblib.load('scaler_dual.pkl')  # Updated to match saved scaler name
    features = ['open', 'high', 'low', 'close', 'tick_volume', 
                'sma_20', 'sma_50', 'rsi', 'bb_upper', 'bb_lower', 'bb_middle', 
                'macd', 'macd_signal', 'macd_hist', 'atr']
    df_scaled = pd.DataFrame(scaler.transform(df[features]), columns=features, index=df.index)
    # Inverse transform all features to original scale
    df_transformed = scaler.inverse_transform(df_scaled)
    # Update DataFrame with original values
    for i, col in enumerate(features):
        df[col] = df_transformed[:, i]
except FileNotFoundError:
    print("Warning: scaler_dual.pkl not found. Using raw values with manual scaling.")
    # Manual scaling: adjust multipliers based on your original price range (e.g., 1800-1900 for XAU/USD)
    price_scale = 1800  # Adjust this to your data's approximate price range
    df['open'] = df['open'] * price_scale
    df['high'] = df['high'] * price_scale
    df['low'] = df['low'] * price_scale
    df['close'] = df['close'] * price_scale
    df['sma_20'] = df['sma_20'] * price_scale
    df['sma_50'] = df['sma_50'] * price_scale
    df['bb_upper'] = df['bb_upper'] * price_scale
    df['bb_lower'] = df['bb_lower'] * price_scale
    df['bb_middle'] = df['bb_middle'] * price_scale
    df['rsi'] = df['rsi'] * 100  # RSI scaled to [0, 100]

# Function to create TradingView-like dashboard
def create_dashboard(df, label_column, title, output_file, show_text_labels=True):
    # Create subplots: 1 for candlestick + indicators, 2 for RSI, 3 for MACD, 4 for ATR
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=('Price & Signals', 'RSI (14)', 'MACD (12,26,9)', 'ATR (14)'),
        row_heights=[0.5, 0.2, 0.2, 0.1]
    )

    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df['time'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Candlestick',
            increasing_line_color='green',
            decreasing_line_color='red'
        ),
        row=1, col=1
    )

    # Continuous close price line
    fig.add_trace(
        go.Scatter(
            x=df['time'], y=df['close'], name='Close Price', line=dict(color='blue', width=1)
        ),
        row=1, col=1
    )

    # SMA (20, 50)
    fig.add_trace(
        go.Scatter(x=df['time'], y=df['sma_20'], name='SMA 20', line=dict(color='orange', width=1.5)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['time'], y=df['sma_50'], name='SMA 50', line=dict(color='purple', width=1.5)),
        row=1, col=1
    )

    # Bollinger Bands
    fig.add_trace(
        go.Scatter(x=df['time'], y=df['bb_upper'], name='BB Upper', line=dict(color='gray', width=1, dash='dash')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['time'], y=df['bb_lower'], name='BB Lower', line=dict(color='gray', width=1, dash='dash')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['time'], y=df['bb_middle'], name='BB Middle', line=dict(color='gray', width=1)),
        row=1, col=1
    )

    # Buy/Sell Signals (Markers)
    buy_signals = df[df[label_column].isin(['strong_buy', 'weak_buy'])]
    sell_signals = df[df[label_column].isin(['strong_sell', 'weak_sell'])]
    
    # Buy signals (green upward triangles)
    fig.add_trace(
        go.Scatter(
            x=buy_signals['time'],
            y=buy_signals['low'] * 0.999,  # Slightly below low
            mode='markers',
            name=f'Buy Signal ({label_column})',
            marker=dict(symbol='triangle-up', color='green', size=10)
        ),
        row=1, col=1
    )

    # Sell signals (red downward triangles)
    fig.add_trace(
        go.Scatter(
            x=sell_signals['time'],
            y=sell_signals['high'] * 1.001,  # Slightly above high
            mode='markers',
            name=f'Sell Signal ({label_column})',
            marker=dict(symbol='triangle-down', color='red', size=10)
        ),
        row=1, col=1
    )

    # Buy/Sell Signals (Text Labels)
    if show_text_labels:
        # Buy text labels
        fig.add_trace(
            go.Scatter(
                x=buy_signals['time'],
                y=buy_signals['low'] * 0.995,  # Slightly below marker
                mode='text',
                text=['Buy'] * len(buy_signals),
                textposition='top center',
                textfont=dict(color='green', size=10),
                showlegend=False
            ),
            row=1, col=1
        )
        # Sell text labels
        fig.add_trace(
            go.Scatter(
                x=sell_signals['time'],
                y=sell_signals['high'] * 1.005,  # Slightly above marker
                mode='text',
                text=['Sell'] * len(sell_signals),
                textposition='bottom center',
                textfont=dict(color='red', size=10),
                showlegend=False
            ),
            row=1, col=1
        )

    # RSI
    fig.add_trace(
        go.Scatter(
            x=df['time'], y=df['rsi'], name='RSI (14)', line=dict(color='blue', width=2),
            mode='lines'
        ),
        row=2, col=1
    )
    # Overbought/oversold lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1, annotation_text="Overbought", annotation_position="top left")
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1, annotation_text="Oversold", annotation_position="bottom left")
    fig.update_yaxes(range=[0, 100], row=2, col=1)

    # MACD
    fig.add_trace(
        go.Scatter(
            x=df['time'], y=df['macd'], name='MACD', line=dict(color='blue', width=2)
        ),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df['time'], y=df['macd_signal'], name='Signal', line=dict(color='orange', width=2)
        ),
        row=3, col=1
    )
    fig.add_trace(
        go.Bar(
            x=df['time'], y=df['macd_hist'], name='MACD Histogram',
            marker_color=df['macd_hist'].apply(lambda x: 'green' if x >= 0 else 'red')
        ),
        row=3, col=1
    )
    fig.add_hline(y=0, line_color="gray", line_width=1, row=3, col=1)

    # ATR
    fig.add_trace(
        go.Scatter(
            x=df['time'], y=df['atr'], name='ATR', line=dict(color='purple', width=2)
        ),
        row=4, col=1
    )

    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title='Time',
        yaxis_title='Price',
        height=1200,
        showlegend=True,
        xaxis_rangeslider_visible=True,  # Enable rangeslider for full data navigation
        template='plotly_dark',
        hovermode='x unified'
    )

    # Update y-axis labels and ranges
    fig.update_yaxes(title_text='Price', row=1, col=1)
    fig.update_yaxes(title_text='RSI', range=[0, 100], row=2, col=1)
    fig.update_yaxes(title_text='MACD', row=3, col=1)
    fig.update_yaxes(title_text='ATR', row=4, col=1)

    # Save to HTML
    fig.write_html(output_file)
    print(f"Dashboard saved as {output_file}")

# Create dashboards for both realistic and perfect labels with text labels
create_dashboard(
    df,
    label_column='label',
    title='TradingView Dashboard - Realistic Trader Labels',
    output_file='realistic_dashboard.html',
    show_text_labels=True
)

create_dashboard(
    df,
    label_column='perfect_label',
    title='TradingView Dashboard - 100% Accurate (Perfect) Labels',
    output_file='perfect_dashboard.html',
    show_text_labels=True
)