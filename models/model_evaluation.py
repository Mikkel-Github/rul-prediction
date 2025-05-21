import argparse
import os

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


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
                    f"unknown labels in column '{col}': {X[col][unknown_mask].unique()}"
                )
                print(" - dropping the rows")
                keep_mask = ~unknown_mask
                X = X[keep_mask]
                y = y[keep_mask]
            X[col] = encoder.transform(X[col])
    return X, y


def plot_rul_results(y_true, y_pred, model_name):
    # scatter plot: true vs predicted
    plt.figure(figsize=(6, 5))
    plt.scatter(y_true, y_pred, alpha=0.3, edgecolors="k")
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], "r--")
    plt.xlabel("True RUL")
    plt.ylabel("Predicted RUL")
    plt.title(f"{model_name} - True vs Predicted RUL")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # histogram of prediction errors
    errors = y_pred - y_true
    plt.figure(figsize=(6, 5))
    plt.hist(errors, bins=50, alpha=0.7, color="teal", edgecolor="black")
    plt.title(f"{model_name} - Prediction Error Distribution")
    plt.xlabel("Prediction Error (Predicted - True)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def evaluate_model(model_path, test_csv_path):
    df = pd.read_csv(test_csv_path)

    model_data = joblib.load(model_path)
    if isinstance(model_data, tuple):
        model, feature_cols = model_data
    else:
        raise ValueError("Model file does not include feature column info.")

    encoders = load_label_encoders(model_path)
    if encoders:
        df, y_true = apply_encoders(df, encoders, df["RUL"])
    else:
        y_true = df["RUL"]

    print(df.dtypes)

    X_test = df[feature_cols]

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    print("\nEvaluation Results:")
    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R²:   {r2:.4f}")

    model_name = os.path.basename(model_path).replace("_model.pkl", "")
    plot_rul_results(y_true, y_pred, model_name)

    return mae, rmse, r2


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", type=str, required=True, help="Path to saved model .pkl file"
    )
    parser.add_argument(
        "--test",
        type=str,
        default="../data-generator/dataset_test.csv",
        help="Path to test CSV file",
    )
    args = parser.parse_args()

    if not os.path.exists(args.model):
        print(f"Model file not found: {args.model}")
    elif not os.path.exists(args.test):
        print(f"Test CSV file not found: {args.test}")
    else:
        evaluate_model(args.model, args.test)
