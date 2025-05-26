import joblib
import pandas as pd
from scripts.encoding import apply_encoders, load_label_encoders
from scripts.preprocess_features import preprocess_single_machine_latest_entry


def predict_rul(machine_id, machines, events):
    print("Starting prediction...")
    df_machines = pd.DataFrame(machines)
    df_events = pd.DataFrame(events)
    ddf = pd.merge(df_events, df_machines, on="machine_id", how="left")
    print("Merged tables")

    print("Running pre-processing features...")
    df = preprocess_single_machine_latest_entry(ddf, machine_id)
    old_df = preprocess_single_machine_latest_entry(ddf, machine_id)

    print("Loading model...")
    model_data = joblib.load("models/xgboost_model.pkl")
    if isinstance(model_data, tuple):
        model, feature_cols = model_data
    else:
        raise ValueError("Model file does not include feature column info")
    print("Loaded model")

    print("Applying encoders...")
    encoders = load_label_encoders("models/xgboost_label_encoders.pkl")
    if encoders:
        df = apply_encoders(df, encoders)

    X = df[feature_cols]

    print("Predicting RUL...")
    prediction = model.predict(X)

    print(prediction)

    df["predicted_rul"] = prediction
    df["component"] = old_df["component"].values

    result = [
        {
            "machine_id": machine_id,
            "results": df[["component", "predicted_rul"]].to_dict(orient="records"),
        }
    ]
    print("Final result:", result)

    return result


def predict_rul_all_machines(machines, events):
    print("Starting batch RUL prediction...")
    df_machines = pd.DataFrame(machines)
    df_events = pd.DataFrame(events)
    ddf = pd.merge(df_events, df_machines, on="machine_id", how="left")

    print("Loading model and encoders...")
    model_data = joblib.load("models/xgboost_model.pkl")
    if isinstance(model_data, tuple):
        model, feature_cols = model_data
    else:
        raise ValueError("Model file does not include feature column info")

    encoders = load_label_encoders("models/xgboost_label_encoders.pkl")

    all_results = []
    for machine_id in df_machines["machine_id"].unique():
        print(f"Processing machine {machine_id}...")
        df = preprocess_single_machine_latest_entry(ddf, machine_id)
        original_df = df.copy()

        if encoders:
            df = apply_encoders(df, encoders)

        X = df[feature_cols]
        prediction = model.predict(X)
        df["predicted_rul"] = prediction
        df["component"] = original_df["component"].values

        machine_result = {
            "machine_id": machine_id,
            "results": df[["component", "component_age", "predicted_rul"]].to_dict(
                orient="records"
            ),
        }
        all_results.append(machine_result)

    print("Predicted for all machines")
    return all_results
