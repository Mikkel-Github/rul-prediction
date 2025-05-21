import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# df = pd.read_csv("../data-generator/dataset_train.csv")
df = pd.read_csv("../data-generator/dataset_3_TRAINING.csv")
df = df.dropna(subset=["RUL"])

categorical_cols = list(df.select_dtypes(include=["object"]).columns)
categorical_cols.append("event_type_encoded")
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

X = df.drop(
    columns=[
        "RUL",
        "machine_id",
        "active_time",
        "prev_failures",
        "is_failure",
        "lifecycle_id",
        "time_since_last_service",
        # "num_services_since_install", # uncomment this for test 5
    ]
)

y = df["RUL"]

model = RandomForestRegressor(
    n_estimators=145,
    max_depth=14,
    min_samples_split=6,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1,
)
model.fit(X, y)

feature_cols = X.columns.tolist()

joblib.dump((model, feature_cols), "random_forest_model.pkl")
joblib.dump(label_encoders, "random_forest_label_encoders.pkl")
print("Random Forest model trained and saved")


# importances = model.feature_importances_
#
# feature_importance_df = pd.DataFrame({"Feature": X.columns, "Importance": importances})
#
# feature_importance_df = feature_importance_df.sort_values(
#     by="Importance", ascending=False
# )
#
# print(feature_importance_df)


############## SHAP Plot


# df_test = pd.read_csv("../data-generator/dataset_3_TEST.csv")
#
# label_encoders = joblib.load("random_forest_label_encoders.pkl")
# for col in label_encoders:
#     if col in df_test.columns:
#         le = label_encoders[col]
#         df_test[col] = le.transform(df_test[col])
#
# categorical_cols_test = df_test.select_dtypes(include=["object"]).columns
# label_encoders_test = {}
# for col in categorical_cols_test:
#     le = LabelEncoder()
#     df_test[col] = le.fit_transform(df_test[col])
#     label_encoders_test[col] = le
#
# X_test = df_test[X.columns]
# import shap
#
# explainer = shap.TreeExplainer(model, X_test)
# shap_values = explainer(X_test)
# shap.summary_plot(shap_values, X_test)
