import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, HoverTool, Select
from bokeh.layouts import column
from bokeh.server.server import Server
from bokeh.io import curdoc

def get_data(timeframe):
    try:
        # Select CSV based on timeframe
        filename = {
            '30min': 'forecast_output_30min.csv',
            '1hour': 'xauusd_1H_full_predictions.csv'
        }.get(timeframe, 'xauusd_m30_full_predictions.csv')  # Default to 30min
        df = pd.read_csv(filename)
        if 'time' not in df.columns or 'actual_price' not in df.columns or 'predicted_price' not in df.columns:
            raise ValueError(f"CSV file {filename} must contain 'time', 'actual_price', and 'predicted_price' columns")
        df['time'] = pd.to_datetime(df['time'])
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
        predicted_price=df['predicted_price'].fillna(method='ffill')  # Forward fill NaN for plotting
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

    # Create figure with dual lines
    p = figure(title="Actual vs Predicted Price", x_axis_label="Time", y_axis_label="Price",
               x_axis_type="datetime", height=600, width=1400, tools="pan,wheel_zoom,box_zoom,reset,save,hover")
    p.line('time', 'actual_price', source=source, line_color="orange", line_width=2, legend_label="Actual Price")
    p.line('time', 'predicted_price', source=source, line_color="green", line_width=2, legend_label="Predicted Price")

    # Configure x-axis formatter
    p.xaxis.formatter = DatetimeTickFormatter(
        hours="%Y-%m-%d %H:%M",
        days="%Y-%m-%d",
        months="%Y-%m",
        years="%Y"
    )

    # Configure hover tool
    p.select_one(HoverTool).tooltips = [
        ("Time", "@time{%Y-%m-%d %H:%M}"),
        ("Actual Price", "@actual_price{0.2f}"),
        ("Predicted Price", "@predicted_price{0.2f}")
    ]
    p.select_one(HoverTool).formatters = {"@time": "datetime"}

    # Add legend
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    # Add dropdown
    dropdown = Select(title="Time Frame", value="30min", options=["30min", "1hour"])
    dropdown.on_change("value", update_dashboard)

    # Layout
    doc.add_root(column(dropdown, p))
    print("Dashboard initialized successfully")

# Set up and run Bokeh server
server = Server({'/': create_dashboard}, num_procs=1)
server.start()

if __name__ == '__main__':
    print('Opening Bokeh application on http://localhost:5006/')
    server.io_loop.start()