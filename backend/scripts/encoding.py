import os

import joblib


def load_label_encoders(model_path):
    encoder_path = model_path.replace("_model.pkl", "_label_encoders.pkl")
    if os.path.exists(encoder_path):
        print(f"Found label encoders: {encoder_path}")
        return joblib.load(encoder_path)
    return None


def apply_encoders(X, encoders, y):
    for col, encoder in encoders.items():
        if col in X.columns:
            known_classes = set(encoder.classes_)
            unknown_mask = ~X[col].isin(known_classes)
            if unknown_mask.any():
                print(
                    f"Unseen labels in column '{col}': {X[col][unknown_mask].unique()}"
                )
                print(" - Dropping these rows.")
                keep_mask = ~unknown_mask
                X = X[keep_mask]
                y = y[keep_mask]
            X[col] = encoder.transform(X[col])
    return X, y


def apply_encoders(X, encoders):
    for col, encoder in encoders.items():
        if col in X.columns:
            known_classes = set(encoder.classes_)
            unknown_mask = ~X[col].isin(known_classes)
            if unknown_mask.any():
                print(
                    f"Unseen labels in column '{col}': {X[col][unknown_mask].unique()}"
                )
                print(" - Dropping these rows.")
                keep_mask = ~unknown_mask
                X = X[keep_mask]
            X[col] = encoder.transform(X[col])
    return X
