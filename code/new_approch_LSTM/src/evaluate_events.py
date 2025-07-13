import sys, os
from pathlib import Path
if '__file__' in globals():
    sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Load test artifacts
models_dir = Path(__file__).resolve().parent.parent / 'models_events'
X_test = np.load(models_dir / 'X_test_events.npy')
y_test = pd.read_csv(models_dir / 'y_test_events.csv')['actual'].values

# Load trained model with custom sum_time
from model_events import sum_time  # import the custom function used in Lambda layer

event_model = load_model(
    models_dir / 'event_model.h5',
    custom_objects={'sum_time': sum_time}
)

# Predict & evaluate
probs = event_model.predict(X_test).ravel()
signals = (probs > 0.5).astype(int)

acc = accuracy_score(y_test, signals)
prec = precision_score(y_test, signals)
rec = recall_score(y_test, signals)
print(f"Eval Results -> Accuracy: {acc:.3f}, Precision: {prec:.3f}, Recall: {rec:.3f}")