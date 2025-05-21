import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
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
        # "num_services_since_install",  # uncomment this for test 5
    ]
)
y = df["RUL"]

model = MLPRegressor(
    hidden_layer_sizes=(100, 50),
    activation="relu",
    solver="adam",
    learning_rate_init=0.001,
    max_iter=500,
    random_state=42,
)
model.fit(X, y)

joblib.dump((model, X.columns.tolist()), "neural_network_model.pkl")
joblib.dump(label_encoders, "neural_network_label_encoders.pkl")
print("Neural network model trained and saved")


############## SHAP plot


# df_test = pd.read_csv("../data-generator/for_tests_TESTING.csv")
#
# label_encoders = joblib.load("neural_network_label_encoders.pkl")
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
# model_fn = lambda x: model.predict(x)
# explainer = shap.KernelExplainer(model_fn, X_test)
# shap_values = explainer.shap_values(X_test)
# shap.summary_plot(shap_values, X_test)
