import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for headless environments

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report


def profit_accuracy(y_true, y_pred):
    # y_true, y_pred: integer labels 0=no_action,1=dec,2=inc
    true_inc = np.sum((y_true == 2) & (y_pred == 2))
    true_dec = np.sum((y_true == 1) & (y_pred == 1))
    false_inc_noact = np.sum((y_true == 0) & (y_pred == 2))
    false_dec_noact = np.sum((y_true == 0) & (y_pred == 1))
    false_inc_dec = np.sum((y_true == 1) & (y_pred == 2))
    false_dec_inc = np.sum((y_true == 2) & (y_pred == 1))

    profit_acc = (true_inc + true_dec) / (
        false_dec_noact + false_inc_noact + true_dec + false_inc_dec + false_dec_inc + true_inc
    )
    return profit_acc

def plot_history(history):
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.legend()
    plt.title('Loss')

    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Train Acc')
    plt.plot(history.history['val_accuracy'], label='Val Acc')
    plt.legend()
    plt.title('Accuracy')

    plt.tight_layout()
    plt.savefig("training_history.png")
    print("Saved training plot as training_history.png")


def print_classification_report(y_true, y_pred):
    print("Confusion Matrix:")
    print(confusion_matrix(y_true, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred))
