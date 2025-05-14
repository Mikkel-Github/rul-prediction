import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor

df = pd.read_csv("../data-generator/dataset_train.csv")
df = df.dropna(subset=["RUL"])

categorical_cols = df.select_dtypes(include=["object"]).columns
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

X = df.drop(
    columns=[
        "RUL",
        "machine_id",
        "prev_failures",
        "is_failure",
        "lifecycle_id",
        "time_since_last_service",
    ]
)
y = df["RUL"]

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

joblib.dump((model, X.columns.tolist()), "xgboost_model.pkl")
joblib.dump(label_encoders, "xgboost_label_encoders.pkl")
print("XGBoost model trained and saved")


# importances = model.feature_importances_
#
# feature_importance_df = pd.DataFrame({"Feature": X.columns, "Importance": importances})
#
# feature_importance_df = feature_importance_df.sort_values(
#     by="Importance", ascending=False
# )
#
# print(feature_importance_df)

###############################


# df_test = pd.read_csv("../dataset_test.csv")
#
# label_encoders = joblib.load("xgboost_label_encoders.pkl")
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
