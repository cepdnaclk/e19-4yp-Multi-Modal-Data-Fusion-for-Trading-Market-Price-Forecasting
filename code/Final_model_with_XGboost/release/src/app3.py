import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, HoverTool
from bokeh.layouts import column
from bokeh.server.server import Server
from bokeh.io import curdoc

def get_data():
    try:
        # Load data from CSV file
        df = pd.read_csv('xauusd_m30_full_predictions.csv')
        if 'time' not in df.columns or 'actual_price' not in df.columns or 'predicted_price' not in df.columns:
            raise ValueError("CSV file must contain 'time', 'actual_price', and 'predicted_price' columns")
        df['time'] = pd.to_datetime(df['time'])
        if df.empty:
            raise ValueError("No data found in the CSV file")
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise

def create_dashboard(doc):
    # Fetch data
    try:
        df = get_data()
        source = ColumnDataSource(data=dict(
            time=df['time'],
            actual_price=df['actual_price'],
            predicted_price=df['predicted_price'].fillna(method='ffill')  # Forward fill NaN for plotting
        ))
    except Exception as e:
        print(f"Failed to load data: {e}")
        doc.add_root(column(figure(title="Error", height=600, width=1400)))
        return

    # Create figure with dual lines
    p = figure(title="Actual vs Predicted Price", x_axis_label="Time", y_axis_label="Price",
               x_axis_type="datetime", height=600, width=1400, tools="pan,wheel_zoom,box_zoom,reset,save,hover")
    p.line('time', 'actual_price', source=source, line_color="green", line_width=2, legend_label="Actual Price")
    p.line('time', 'predicted_price', source=source, line_color="orange", line_width=2, legend_label="Predicted Price", line_dash="dashed")

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

    # Layout
    doc.add_root(column(p))
    print("Dashboard initialized successfully")

# Set up and run Bokeh server
server = Server({'/': create_dashboard}, num_procs=1)
server.start()

if __name__ == '__main__':
    print('Opening Bokeh application on http://localhost:5006/')
    server.io_loop.start()