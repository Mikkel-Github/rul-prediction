import joblib
import matplotlib.pyplot as plt
import pandas as pd
import shap
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv("../data-generator/dataset_train.csv")
df = df.dropna(subset=["RUL"])

X = df.drop(
    columns=[
        "RUL",
        "machine_id",
        "prev_failures",
        "is_failure",
        "lifecycle_id",
    ]
)

y = df["RUL"]

categorical_features = ["component", "machine_type"]
numerical_features = [
    "component_age",
    "num_services_since_install",
    "component_age_x_services",
    "time_since_last_service",
    "event_type_encoded",
]

preprocessor = ColumnTransformer(
    [
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numerical_features),
    ]
)

model = Pipeline([("preprocessor", preprocessor), ("regressor", LinearRegression())])
model.fit(X, y)

feature_cols = X.columns.tolist()
joblib.dump((model, feature_cols), "linear_regression_model.pkl")
print("Model trained and saved")
