# dashboard.py

import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

print("🚀 dashboard.py starting up…")      # <— sanity-check

# Load your data once
df = pd.read_csv('forex_data_with_labels.csv', parse_dates=['time'])
df.set_index('time', inplace=True)

app = Dash(__name__)
app.title = "Trading Dashboard"

app.layout = html.Div([
    dcc.Graph(
        id='chart',
        config={'scrollZoom': True},
        style={'height': '90vh', 'width': '100vw'}
    )
])

@app.callback(
    Output('chart', 'figure'),
    [Input('chart', 'relayoutData')]
)
def update_figure(relayout):
    # print(relayout)  # uncomment to see zoom events in console
    if relayout and 'xaxis.range[0]' in relayout:
        t0 = pd.to_datetime(relayout['xaxis.range[0]'])
        t1 = pd.to_datetime(relayout['xaxis.range[1]'])
        dff = df.loc[t0:t1]
    else:
        dff = df

    # Build the 3-row figure
    fig = make_subplots(rows=3, cols=1,
                        shared_xaxes=True,
                        row_heights=[0.5,0.2,0.3],
                        vertical_spacing=0.02)

    # Candlesticks + BB
    fig.add_trace(go.Candlestick(
        x=dff.index, open=dff.open, high=dff.high,
        low=dff.low, close=dff.close,
        increasing_line_color='green',
        decreasing_line_color='red',
        name='Price'
    ), row=1, col=1)
    fig.add_trace(go.Scattergl(
        x=dff.index, y=dff.bb_upper, mode='lines',
        line=dict(color='gray', dash='dash'), name='BB Upper'
    ), row=1, col=1)
    fig.add_trace(go.Scattergl(
        x=dff.index, y=dff.bb_lower, mode='lines',
        line=dict(color='gray', dash='dash'), name='BB Lower'
    ), row=1, col=1)

    # Perfect-label signals
    buys  = dff[dff.perfect_label=='strong_buy']
    sells = dff[dff.perfect_label=='strong_sell']
    fig.add_trace(go.Scattergl(
        x=buys.index, y=buys.low,
        mode='markers', marker_symbol='triangle-up',
        marker_color='blue', marker_size=10,
        name='Perfect Buy'
    ), row=1, col=1)
    fig.add_trace(go.Scattergl(
        x=sells.index, y=sells.high,
        mode='markers', marker_symbol='triangle-down',
        marker_color='magenta', marker_size=10,
        name='Perfect Sell'
    ), row=1, col=1)

    # RSI 0–100
    fig.add_trace(go.Scattergl(
        x=dff.index, y=dff.rsi * 100,
        mode='lines', line=dict(color='purple'), name='RSI'
    ), row=2, col=1)
    fig.add_hline(y=70, line=dict(color='gray', dash='dash'), row=2, col=1)
    fig.add_hline(y=30, line=dict(color='gray', dash='dash'), row=2, col=1)
    fig.update_yaxes(range=[0,100], row=2, col=1)

    # MACD & signal
    fig.add_trace(go.Scattergl(
        x=dff.index, y=dff.macd, mode='lines',
        line=dict(color='blue'), name='MACD'
    ), row=3, col=1)
    fig.add_trace(go.Scattergl(
        x=dff.index, y=dff.macd_signal, mode='lines',
        line=dict(color='red'), name='Signal'
    ), row=3, col=1)

    fig.update_layout(
        height=900,
        showlegend=True,
        dragmode='zoom',
        xaxis_rangeslider_visible=False,
        title='XAU/USD 30m — Perfect-Label Signals'
    )
    fig.update_xaxes(visible=False, row=1, col=1)
    fig.update_xaxes(visible=False, row=2, col=1)
    return fig

if __name__ == '__main__':
    print("🚀 Starting Dash server at http://127.0.0.1:8050")
    app.run_server(debug=False, port=8050)
