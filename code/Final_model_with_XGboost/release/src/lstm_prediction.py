import sqlite3
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
import os

# Load and preprocess data
def get_data():
    conn = sqlite3.connect('financial_data.db')
    try:
        query = "SELECT time, price, candlebody, candleupperwick, candlelowerwick FROM financial_data ORDER BY time ASC LIMIT 10000"
        df = pd.read_sql_query(query, conn)
        df['time'] = pd.to_datetime(df['time'])
        if df.empty:
            raise ValueError("No data found in the database")
        # Derive OHLC with element-wise conditional
        df['open'] = df['price'] - (df['candlebody'].abs() / 2) * np.where(df['candlebody'] >= 0, 1, -1)
        df['high'] = df['price'] + df['candleupperwick']
        df['low'] = df['price'] - df['candlelowerwick']
        df['close'] = df['price']
        # Validate and clean
        df = df.dropna()
        df = df[(df['high'] >= df['low']) & (df['high'] >= df['open']) & (df['high'] >= df['close']) &
                (df['low'] <= df['open']) & (df['low'] <= df['close'])]
        if df.empty:
            raise ValueError("No valid OHLC data after validation")
        print(f"Loaded {len(df)} valid data points")
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise
    finally:
        conn.close()

# Create sequences for LSTM
def create_sequences(data, seq_length, forecast_horizon):
    X, y = [], []
    for i in range(len(data) - seq_length - forecast_horizon + 1):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length + forecast_horizon - 1, 3])  # Predict close after horizon
    return np.array(X), np.array(y)

# Main execution
if __name__ == '__main__':
    # Get and prepare data
    df = get_data()
    data = df[['open', 'high', 'low', 'close']].values
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    # Parameters
    seq_length = 60  # 60 minutes (1 hour) of history
    forecast_horizon = 240  # 240 minutes (4 hours) ahead
    X, y = create_sequences(data_scaled, seq_length, forecast_horizon)
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # Build LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(seq_length, 4)))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    print("Training model...")
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test), verbose=1)

    # Predict
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(np.hstack((np.zeros((len(predictions), 3)), predictions)))
    y_test_inv = scaler.inverse_transform(np.hstack((np.zeros((len(y_test), 3)), y_test.reshape(-1, 1))))

    # Evaluate
    mse = np.mean((predictions - y_test_inv) ** 2)
    print(f"Mean Squared Error: {mse:.2f}")
    print("Note: High MSE (e.g., >1000) suggests the model may need tuning (e.g., more epochs, layers) or better feature engineering.")

    # Simple trading signal
    current_price = y_test_inv[-1][0]  # Last actual close
    predicted_price = predictions[-1][0]
    threshold = current_price * 0.01  # 1% threshold
    signal = "Buy" if predicted_price > current_price + threshold else "Hold"
    print(f"Current Price: {current_price:.2f}, Predicted Price: {predicted_price:.2f}, Signal: {signal}")

    # Plot with fallback to save file
    try:
        plt.figure(figsize=(12, 6))
        plt.plot(y_test_inv, label='Actual Close')
        plt.plot(predictions, label='Predicted Close')
        plt.title('LSTM Price Prediction')
        plt.xlabel('Time Steps')
        plt.ylabel('Price')
        plt.legend()
        plt.savefig('lstm_prediction.png')  # Save plot to file
        print("Plot saved as 'lstm_prediction.png' due to Tkinter issue.")
    except Exception as e:
        print(f"Failed to display plot: {e}. Plot saved as 'lstm_prediction.png'.")
        plt.savefig('lstm_prediction.png')
    finally:
        plt.close()