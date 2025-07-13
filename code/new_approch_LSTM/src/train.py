# src/train.py

import sys, os
# Ensure local modules are importable when running as a script
if '__file__' in globals():
    sys.path.insert(0, os.path.dirname(__file__))

import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
import kerastuner as kt
from sklearn.model_selection import train_test_split

from data_prep import load_data
from indicators import add_indicators
from dataset import build_sequences
from model import lstm_attention_model

def run_training():
    # Load data and add technical indicators
    df = load_data()                        # no args required
    df = add_indicators(df)

    # Feature setup
    feats = ['Close', 'RSI', 'MACD', 'MACD_sig', 'BB_upper', 'BB_lower', 'Volume']
    X, y, scaler = build_sequences(df, feats, window=50)

    # Time-based 80/10/10 split
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, shuffle=False
    )

    # Early stopping callback
    es = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    # Build and train model
    model = lstm_attention_model(window=X.shape[1], feature_dim=X.shape[2])
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=100,
        batch_size=64,
        callbacks=[es]
    )

    # Save the trained model
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, 'fx_lstm_attn.h5')
    model.save(model_path)
    print(f"Model saved to {model_path}")

    return model, scaler, X_test, y_test

if __name__ == '__main__':
    run_training()
