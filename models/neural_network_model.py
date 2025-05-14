import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import LabelEncoder

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
