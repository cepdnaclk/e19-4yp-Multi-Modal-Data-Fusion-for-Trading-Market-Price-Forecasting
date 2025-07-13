# src/export_predictions.py

import sys, os
from pathlib import Path

if '__file__' in globals():
    sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

from dataset_events import build_event_dataset
from model_events import sum_time  # for custom_objects

def export_predictions(
    lookback: int = 50,
    lookahead: int = 5,
    model_dir: str = '../models_events',
    out_csv: str = '../outputs/predictions.csv'
):
    # 1) Rebuild the event dataset (X, y, timestamps)
    X, y_true, times = build_event_dataset(lookback, lookahead)

    # 2) Load the trained model
    model_path = Path(__file__).resolve().parent.parent / model_dir / 'event_model.h5'
    model = load_model(
        model_path,
        custom_objects={'sum_time': sum_time}
    )

    # 3) Get prediction probabilities & binary signals
    probs = model.predict(X).ravel()
    signals = (probs > 0.5).astype(int)

    # 4) Build DataFrame
    df = pd.DataFrame({
        'time': pd.to_datetime(times),
        'actual': y_true,
        'probability': probs,
        'signal': signals
    })
    # sort by time just in case
    df.sort_values('time', inplace=True)

    # 5) Save to CSV
    out_path = Path(__file__).resolve().parent.parent / out_csv
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Exported {len(df)} predictions to {out_path}")

if __name__ == '__main__':
    export_predictions()
