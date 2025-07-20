import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, HoverTool
from bokeh.layouts import column
from bokeh.server.server import Server
from bokeh.io import curdoc
from bokeh.palettes import Category10

def get_data():
    try:
        # Load data from both CSV files
        df1 = pd.read_csv('test_with_predictions.csv')
        df2 = pd.read_csv('xauusd_M1_full_predictions.csv')
        
        # Ensure required columns exist
        if 'date' not in df1.columns or 'price' not in df1.columns or 'predicted_price' not in df1.columns:
            raise ValueError("test_with_predictions.csv must contain 'date', 'price', and 'predicted_price' columns")
        if 'time' not in df2.columns or 'actual_price' not in df2.columns or 'predicted_price' not in df2.columns:
            raise ValueError("xauusd_M1_full_predictions.csv must contain 'time', 'actual_price', and 'predicted_price' columns")

        # Align and convert dates
        df1['date'] = pd.to_datetime(df1['date'])
        df2['time'] = pd.to_datetime(df2['time'])
        df1 = df1.rename(columns={'date': 'time', 'price': 'actual_price_from_df1'})  # Temporary rename

        # Use actual_price from df2 and merge predicted prices
        df = pd.merge(df2[['time', 'actual_price', 'predicted_price']], 
                      df1[['time', 'predicted_price']].rename(columns={'predicted_price': 'predicted_price_with_macro'}),
                      on='time', how='outer')
        
        # Fill missing values
        df['actual_price'] = df['actual_price'].fillna(method='ffill')  # Use df2's actual_price
        df['predicted_price_with_macro'] = df['predicted_price_with_macro'].fillna(method='ffill')
        df['predicted_price'] = df['predicted_price'].fillna(method='ffill')  # Without macro

        if df.empty:
            raise ValueError("No data found after merging CSV files")
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise

def create_dashboard(doc):
    # Fetch and prepare data
    try:
        df = get_data()
        source = ColumnDataSource(data=dict(
            time=df['time'],
            actual_price=df['actual_price'],
            predicted_price_with_macro=df['predicted_price_with_macro'],
            predicted_price=df['predicted_price']  # Without macro
        ))
    except Exception as e:
        print(f"Failed to load data: {e}")
        doc.add_root(column(figure(title="Error", height=500, width=1000)))
        return

    # Create figure with three lines
    p = figure(title="Monthly Price Prediction: Actual vs Predicted", 
               x_axis_label="Month", 
               y_axis_label="Price (USD)", 
               x_axis_type="datetime", 
               height=500, 
               width=1000, 
               tools="pan,wheel_zoom,box_zoom,reset,save,hover,undo,redo",
               toolbar_location="above",
               active_scroll="wheel_zoom")
    p.line('time', 'actual_price', source=source, line_color=Category10[3][0], line_width=2, legend_label="Actual Price")
    p.line('time', 'predicted_price_with_macro', source=source, line_color=Category10[3][1], line_width=2, legend_label="Predicted Price (With Macro)")
    p.line('time', 'predicted_price', source=source, line_color=Category10[3][2], line_width=2, legend_label="Predicted Price (Without Macro)", line_dash="dashed")

    # Enhance plot appearance
    p.title.text_font_size = "20px"
    p.xaxis.axis_label_text_font_size = "14px"
    p.yaxis.axis_label_text_font_size = "14px"
    p.xaxis.major_label_text_font_size = "12px"
    p.yaxis.major_label_text_font_size = "12px"
    p.background_fill_color = "#f5f5f5"
    p.border_fill_color = "white"
    p.grid.grid_line_color = "#e0e0e0"
    p.legend.label_text_font_size = "12px"
    p.legend.background_fill_color = "white"
    p.legend.border_line_color = "black"
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    # Configure x-axis formatter for monthly data
    p.xaxis.formatter = DatetimeTickFormatter(
        months="%Y-%m",
        years="%Y"
    )

    # Configure hover tool
    p.select_one(HoverTool).tooltips = [
        ("Month", "@time{%Y-%m}"),
        ("Actual Price", "@actual_price{0.2f} USD"),
        ("Predicted (With Macro)", "@predicted_price_with_macro{0.2f} USD"),
        ("Predicted (Without Macro)", "@predicted_price{0.2f} USD")
    ]
    p.select_one(HoverTool).formatters = {"@time": "datetime"}

    # Layout
    layout = column(p, sizing_mode="stretch_width")
    doc.add_root(layout)
    print("Dashboard initialized successfully")

# Set up and run Bokeh server
server = Server({'/': create_dashboard}, num_procs=1)
server.start()

if __name__ == '__main__':
    print('Opening Bokeh application on http://localhost:5006/')
    server.io_loop.start()