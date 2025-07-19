import sqlite3
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, HoverTool
from bokeh.layouts import column
from bokeh.server.server import Server
from bokeh.io import curdoc
from datetime import datetime

def get_data():
    conn = sqlite3.connect('financial_data.db')
    try:
        query = "SELECT time, price FROM financial_data ORDER BY time DESC"
        df = pd.read_sql_query(query, conn)
        df['time'] = pd.to_datetime(df['time'])
        if df.empty:
            raise ValueError("No data found in the database")
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise
    finally:
        conn.close()

def create_dashboard(doc):
    # Fetch data
    try:
        df = get_data()
        source = ColumnDataSource(data=dict(
            time=df['time'],
            price=df['price']
        ))
    except Exception as e:
        print(f"Failed to load data: {e}")
        doc.add_root(column(figure(title="Error", height="80%", width="80%")))
        return

    # Create figure with default toolbar
    p = figure(title="Price Time Series", x_axis_label="Time", y_axis_label="Price",
               x_axis_type="datetime", height=600, width=1400, tools="pan,wheel_zoom,box_zoom,reset,save,hover")
    p.line('time', 'price', source=source, line_color="blue", line_width=2)

    # Configure x-axis formatter
    p.xaxis.formatter = DatetimeTickFormatter(
        hours="%Y-%m-%d %H:%M",
        days="%Y-%m-%d",
        months="%Y-%m",
        years="%Y"
    )

    # Configure hover tool
    p.select_one(HoverTool).tooltips = [("Time", "@time{%Y-%m-%d %H:%M}"), ("Price", "@price{0.2f}")]
    p.select_one(HoverTool).formatters = {"@time": "datetime"}

    # Layout
    doc.add_root(column(p))
    print("Dashboard initialized successfully")

# Set up and run Bokeh server
server = Server({'/': create_dashboard}, num_procs=1)
server.start()

if __name__ == '__main__':
    print('Opening Bokeh application on http://localhost:5006/')
    server.io_loop.start()