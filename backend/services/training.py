import os

import pandas as pd
from scripts.preprocess_features import preprocess_data

# from models.random_forest_model import train_random_forest_model
from models.xgboost_model import train_xgboost_model


def train_model(machines, events):
    print("Training...")

    df_machines = pd.DataFrame(machines)
    df_events = pd.DataFrame(events)
    df = pd.merge(df_events, df_machines, on="machine_id", how="left")
    print("Merged tables")

    features = preprocess_data(df)
    print("Preprocessed the data")

    train_xgboost_model(features)
    # train_random_forest_model(features)
    print("Trained the model")
