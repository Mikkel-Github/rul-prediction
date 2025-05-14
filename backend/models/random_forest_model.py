import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder


def train_random_forest_model(features: pd.DataFrame, save_path="./models"):
    categorical_cols = features.select_dtypes(include=["object"]).columns
    label_encoders = {}

    for col in categorical_cols:
        le = LabelEncoder()
        features[col] = le.fit_transform(features[col])
        label_encoders[col] = le

    X = features.drop(
        columns=[
            "RUL",
            "machine_id",
            "prev_failures",
            "is_failure",
            "lifecycle_id",
        ]
    )
    y = features["RUL"]

    model = RandomForestRegressor(
        n_estimators=145,
        max_depth=14,
        min_samples_split=6,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X, y)

    print("Done training model")

    feature_cols = X.columns.tolist()

    joblib.dump((model, feature_cols), save_path + "/random_forest_model.pkl")
    joblib.dump(label_encoders, save_path + "/random_forest_encoders.pkl")
    print("Random Forest model trained and savedd")
