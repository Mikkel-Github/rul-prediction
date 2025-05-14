import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor


def train_xgboost_model(features: pd.DataFrame, save_path="./models"):
    print("Training XGBoost Model...")

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
            "time_since_last_service",
        ]
    )
    y = features["RUL"]

    model = XGBRegressor(
        objective="reg:squarederror",
        n_estimators=288,
        max_depth=7,
        learning_rate=0.04174777526056224,
        subsample=0.7567648345914519,
        colsample_bytree=0.9067224727260939,
        gamma=3.532266575167278,
        reg_alpha=0.10038637447471692,
        reg_lambda=0.9106249447089104,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X, y)

    print("Done training model")

    joblib.dump((model, X.columns.tolist()), save_path + "/xgboost_model.pkl")
    joblib.dump(label_encoders, save_path + "/xgboost_label_encoders.pkl")
    print("XGBoost model trained and saved")
