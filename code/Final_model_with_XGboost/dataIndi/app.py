import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, HoverTool, Legend
from bokeh.layouts import column
from bokeh.server.server import Server
from bokeh.io import curdoc

def get_data():
    try:
        # Load dataset (make sure columns: time, actual_price, predicted_price)
        df = pd.read_csv('forecast_output.csv')  # <-- Update path as needed
        df['time'] = pd.to_datetime(df['time'])

        required_cols = {'time', 'actual_price', 'predicted_price'}
        if not required_cols.issubset(df.columns):
            raise ValueError("CSV must contain columns: time, actual_price, predicted_price")

        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise

def create_dashboard(doc):
    try:
        df = get_data()

        source = ColumnDataSource(data=dict(
            time=df['time'],
            actual=df['actual_price'],
            predicted=df['predicted_price']
        ))
    except Exception as e:
        print(f"Failed to load data: {e}")
        doc.add_root(column(figure(title="Error Loading Data")))
        return

    p = figure(title="Gold Price Forecast: Actual vs Predicted",
               x_axis_type="datetime", height=600, width=1400,
               x_axis_label="Time", y_axis_label="Price (USD)",
               tools="pan,wheel_zoom,box_zoom,reset,save,hover")

    actual_line = p.line('time', 'actual', source=source, color="blue", line_width=2, legend_label="Actual Price")
    predicted_line = p.line('time', 'predicted', source=source, color="green", line_width=2, legend_label="Predicted Price")

    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    p.xaxis.formatter = DatetimeTickFormatter(
        minutes="%Y-%m-%d %H:%M",
        hours="%Y-%m-%d %H:%M",
        days="%Y-%m-%d",
        months="%Y-%m",
        years="%Y"
    )

    hover = p.select_one(HoverTool)
    hover.tooltips = [("Time", "@time{%Y-%m-%d %H:%M}"), ("Actual", "@actual{0.2f}"), ("Predicted", "@predicted{0.2f}")]
    hover.formatters = {"@time": "datetime"}

    doc.add_root(column(p))
    print("✅ Bokeh dashboard initialized")

# Run Bokeh server
server = Server({'/': create_dashboard}, num_procs=1, port=5006)
server.start()

if __name__ == '__main__':
    print("Opening Bokeh app at http://localhost:5006/")
    server.io_loop.start()
