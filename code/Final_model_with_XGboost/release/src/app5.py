import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, HoverTool, Select, WheelZoomTool
from bokeh.layouts import column
from bokeh.server.server import Server
from bokeh.io import curdoc
from scipy.signal import savgol_filter

def get_data(timeframe):
    try:
        filename_map = {
            '30min': 'xauusd_m30_full_predictions.csv',
            '1hour': 'xauusd_1H_full_predictions.csv',
            '1Month (with macro)': 'xauusd_M1_full_predictions_withmacro.csv',
            '1Month (clean)': 'xauusd_M1_full_predictions_withoutmacro.csv',
            '1Month (with indicators)': 'xauusd_M1_full_predictions_with_indicators.csv',
            '1Month (hybrid)': 'xauusd_M1_full_predictions_with_hybrid.csv'
        }
        filename = filename_map.get(timeframe, 'xauusd_m30_full_predictions.csv')
        df = pd.read_csv(filename)
        if 'time' not in df.columns or 'actual_price' not in df.columns or 'predicted_price' not in df.columns:
            raise ValueError(f"CSV file {filename} must contain 'time', 'actual_price', and 'predicted_price'")
        df['time'] = pd.to_datetime(df['time'])

        # Apply smoothing only for 30min and 1hour views
        if timeframe in ['30min', '1hour']:
            df['actual_price'] = savgol_filter(df['actual_price'], window_length=9, polyorder=2)

        if df.empty:
            raise ValueError(f"No data found in {filename}")
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise


# Define source as a global variable
source = None

def update_dashboard(attr, old, new):
    global source
    df = get_data(new)
    source.data = dict(
        time=df['time'],
        actual_price=df['actual_price'],
        predicted_price=df['predicted_price'] # Forward fill for safety
    )

def create_dashboard(doc):
    global source
    # Initial data (30min by default)
    df = get_data('30min')
    source = ColumnDataSource(data=dict(
        time=df['time'],
        actual_price=df['actual_price'],
        predicted_price=df['predicted_price'].fillna(method='ffill')
    ))

    # Create figure with default wheel zoom
    p = figure(
        title="Actual vs Predicted Price",
        x_axis_label="Time", y_axis_label="Price",
        x_axis_type="datetime", height=600, width=1400,
        tools="pan,box_zoom,reset,save,hover"
    )

    # Wheel zooms
    wheel_zoom_both = WheelZoomTool(dimensions='both')
    wheel_zoom_y = WheelZoomTool(dimensions='height')

    # Add both zoom tools
    p.add_tools(wheel_zoom_both, wheel_zoom_y)

    # Set default to both-axes zoom
    p.toolbar.active_scroll = wheel_zoom_both

    # Lines
    p.line('time', 'actual_price', source=source, line_color="orange", line_width=2, legend_label="Actual Price")
    p.line('time', 'predicted_price', source=source, line_color="green", line_width=2, legend_label="Predicted Price")

    # X-axis formatting
    p.xaxis.formatter = DatetimeTickFormatter(
        hours="%Y-%m-%d %H:%M",
        days="%Y-%m-%d",
        months="%Y-%m",
        years="%Y"
    )

    # Hover
    p.select_one(HoverTool).tooltips = [
        ("Time", "@time{%Y-%m-%d %H:%M}"),
        ("Actual Price", "@actual_price{0.2f}"),
        ("Predicted Price", "@predicted_price{0.2f}")
    ]
    p.select_one(HoverTool).formatters = {"@time": "datetime"}

    # Legend
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    # Dropdown for timeframe selection
    dropdown = Select(
        title="Time Frame",
        value="30min",
        options=["30min", "1hour", "1Month (with macro)", "1Month (clean)", "1Month (with indicators)", "1Month (hybrid)"]
    )
    dropdown.on_change("value", update_dashboard)

    # Layout
    doc.add_root(column(dropdown, p))
    print("✅ Dashboard initialized")

# Run Bokeh server
server = Server({'/': create_dashboard}, num_procs=1)
server.start()

if __name__ == '__main__':
    print('🌐 Opening Bokeh application at http://localhost:5006/')
    server.io_loop.start()
