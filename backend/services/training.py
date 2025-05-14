import os

import pandas as pd

# from models.random_forest_model import train_random_forest_model
from models.xgboost_model import train_xgboost_model
from scripts.preprocess_features import preprocess_data


def train_model(machines, events):
    print("Training...")

    df_machines = pd.DataFrame(machines)
    df_events = pd.DataFrame(events)
    df = pd.merge(df_events, df_machines, on="machine_id", how="left")
    print("Merged tables")

    features = preprocess_data(df)
    print("Preprocessed the data")

    export_average_lifespans(features)
    print("Exported average lifespans")

    train_xgboost_model(features)
    # train_random_forest_model(features)
    print("Trained the model")


def export_average_lifespans(df_features):
    print("Calculating average lifespans...")

    failure_events = df_features[df_features["is_failure"] == 1]

    avg_lifespan_df = (
        failure_events.groupby(["machine_type", "component"])["component_age"]
        .mean()
        .reset_index()
    )
    avg_lifespan_df.rename(columns={"component_age": "avg_lifespan"}, inplace=True)

    output_path = os.path.join("data", "average_lifespan.csv")
    os.makedirs("data", exist_ok=True)
    avg_lifespan_df.to_csv(output_path, index=False)
    print(f"Saved average lifespans to {output_path}")
