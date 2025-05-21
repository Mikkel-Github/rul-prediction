import joblib
import matplotlib.pyplot as plt
import pandas as pd
import shap
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# df = pd.read_csv("../data-generator/dataset_train.csv")
df = pd.read_csv("../data-generator/dataset_4_TRAINING.csv")
df = df.dropna(subset=["RUL"])

X = df.drop(
    columns=[
        "RUL",
        "machine_id",
        "active_time",
        "prev_failures",
        "is_failure",
        "lifecycle_id",
        "time_since_last_service",
        # "num_services_since_install",  # uncomment this for test 5
    ]
)

y = df["RUL"]

categorical_features = ["component", "machine_type", "event_type_encoded"]
numerical_features = [
    "component_age",
    "num_services_since_install",  # comment this for test 5
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


############## PRINT THE FUNCITON
# regressor = model.named_steps["regressor"]
#
# import numpy as np
#
# feature_names_after_preprocessing = model.named_steps[
#     "preprocessor"
# ].get_feature_names_out(feature_cols)
#
# coefficients = regressor.coef_
# intercept = regressor.intercept_
#
# print("RUL =")
# for name, coef in zip(feature_names_after_preprocessing, coefficients):
#     print(f"  + ({coef:.4f}) * {name}")
# print(f"  + ({intercept:.4f})")


############## SHAP PLOT

# df_test = pd.read_csv("../data-generator/for_tests_TESTING.csv")
#
#
# categorical_features = ["component", "machine_type", "event_type_encoded"]
# numerical_features = [
#     "component_age",
#     "num_services_since_install",
# ]
#
# preprocessor = ColumnTransformer(
#     [
#         ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
#         ("num", "passthrough", numerical_features),
#     ]
# )
#
# X_test = df_test[X.columns]
#
# import shap
#
# X_transformed = model.named_steps["preprocessor"].transform(X_test)
# if hasattr(X_transformed, "toarray"):
#     X_transformed = X_transformed.toarray()
#
# one_hot_encoding = model.named_steps["preprocessor"].named_transformers_["cat"]
# ohe_feature_names = one_hot_encoding.get_feature_names_out(categorical_features)
# feature_names = list(ohe_feature_names) + numerical_features
#
# explainer = shap.LinearExplainer(
#     model.named_steps["regressor"], X_transformed, feature_names=feature_names
# )
# shap_values = explainer.shap_values(X_transformed)
#
# shap.summary_plot(shap_values, X_transformed, feature_names=feature_names)
