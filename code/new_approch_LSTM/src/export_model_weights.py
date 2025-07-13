# src/export_model_weights.py

import os
import h5py
import numpy as np
import pandas as pd
from pathlib import Path

def export_weights(h5_path: str, out_dir: str = 'outputs/weights'):
    """
    Opens the given .h5 model file, iterates through every layer's weights,
    and writes each weight array to a CSV file:
      outputs/weights/{layer_name}__{weight_name}.csv
    """
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    with h5py.File(h5_path, 'r') as f:
        # Navigate into the weights group
        # Typical key: 'model_weights'
        if 'model_weights' in f:
            weights_group = f['model_weights']
        else:
            # fallback: entire file is weights
            weights_group = f

        for layer_name in weights_group:
            layer_grp = weights_group[layer_name]
            for weight_name in layer_grp:
                ds = layer_grp[weight_name]
                data = np.array(ds)
                # Flatten 1D or 2D arrays into DataFrame
                if data.ndim == 1:
                    df = pd.DataFrame(data, columns=[weight_name])
                else:
                    # name columns as weight_name_col0, col1, …
                    cols = [f"{weight_name}_{i}" for i in range(data.shape[1])]
                    df = pd.DataFrame(data, columns=cols)

                csv_file = out_path / f"{layer_name}__{weight_name}.csv"
                df.to_csv(csv_file, index=False)
                print(f"Exported {layer_name}/{weight_name} → {csv_file}")

if __name__ == '__main__':
    # adjust the path if needed
    model_file = Path(__file__).resolve().parent.parent / 'models_events' / 'event_model.h5'
    export_weights(str(model_file))
