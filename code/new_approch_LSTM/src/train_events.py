import sys, os
if '__file__' in globals():
    sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.model_selection import train_test_split
from pathlib import Path  

from dataset_events import build_event_dataset
from model_events import build_event_model


def run_event_training(lookback=50, lookahead=5, test_size=0.2):
    X, y, times = build_event_dataset(lookback, lookahead)
    idx = np.arange(len(y))
    train_idx, temp_idx = train_test_split(idx, test_size=test_size, shuffle=False)
    val_idx, test_idx = train_test_split(temp_idx, test_size=0.5, shuffle=False)

    X_train, y_train = X[train_idx], y[train_idx]
    X_val, y_val     = X[val_idx],   y[val_idx]
    X_test, y_test   = X[test_idx],  y[test_idx]

    es = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    rlrop = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6)

    model = build_event_model(lookback, X.shape[2])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Precision(name='prec'), tf.keras.metrics.Recall(name='rec')]
    )

    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=1, batch_size=32,
        callbacks=[es, rlrop]
    )

    out = Path(__file__).resolve().parent.parent / 'models_events'
    os.makedirs(out, exist_ok=True)
    model.save(out / 'event_model.h5')
    pd.DataFrame({'time': np.array(times)[test_idx], 'actual': y_test}).to_csv(out / 'y_test_events.csv', index=False)
    np.save(out / 'X_test_events.npy', X_test)
    print(f"Saved event model & data to {out}")

if __name__ == '__main__':
    run_event_training()