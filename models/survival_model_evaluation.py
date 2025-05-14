import argparse
import os

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index


def evaluate_survival_model(model_path, test_path):
    df = pd.read_csv(test_path)

    model = joblib.load(model_path)
    print(f"Loaded survival model")

    # Load and apply label encoders
    encoder_path = model_path.replace("_model.pkl", "_label_encoders.pkl")
    if os.path.exists(encoder_path):
        encoders = joblib.load(encoder_path)
        for col, encoder in encoders.items():
            if col in df.columns:
                df[col] = encoder.transform(df[col])
        print(f"Applied label encoders")
    else:
        print("No label encoders found")

    df = df.rename(columns={"RUL": "duration", "event_type_encoded": "event"})

    if "duration" not in df.columns or "event" not in df.columns:
        raise ValueError(
            "Test data must include 'RUL' (renamed to 'duration') and 'event_type_encoded' (renamed to 'event')."
        )

    X_test = df[model.params_.index]
    durations = df["duration"]
    events = df["event"]

    partial_hazards = model.predict_partial_hazard(X_test)

    c_index = concordance_index(durations, -partial_hazards, events)
    print(f"\nConcordance Index (C-Index): {c_index:.4f}")

    # risk scores vs. actual RUL
    plt.figure(figsize=(10, 6))
    plt.scatter(partial_hazards, durations, alpha=0.5)
    plt.title("Predicted Risk Score vs. Actual Remaining Useful Life")
    plt.xlabel("Predicted Risk (Partial Hazard)")
    plt.ylabel("Actual RUL")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("survival_model_risk_vs_rul.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Path to the model (pkl file).",
    )
    parser.add_argument(
        "--data", type=str, required=True, help="Path to the test dataset."
    )
    args = parser.parse_args()

    evaluate_survival_model(args.model, args.data)
