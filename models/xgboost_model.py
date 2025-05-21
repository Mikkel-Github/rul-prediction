import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor

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

model = XGBRegressor(
    objective="reg:squarederror",
    tree_method="hist",
    n_estimators=233,
    max_depth=5,
    learning_rate=0.07111840279402384,
    subsample=0.7570820485125909,
    colsample_bytree=0.7152053904856466,
    gamma=1.1011024170064456,
    reg_alpha=0.8510615949227622,
    reg_lambda=2.0611507000282665,
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


############################### SHAP plot


# df_test = pd.read_csv("../data-generator/for_tests_TESTING.csv")
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
