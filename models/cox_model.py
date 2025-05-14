import joblib
import pandas as pd
from lifelines import CoxPHFitter
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("../data-generator/dataset_train.csv")
df = df.dropna(subset=["RUL"])

df["event_occurred"] = (df["event_type_encoded"] == 2).astype(int)
df = df[df["component_age"] > 0]

categorical_cols = df.select_dtypes(include=["object"]).columns
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

features = [
    "machine_type",
    "component",
    "component_age",
    # "prev_failures",
    "num_services_since_install",
    "component_age_x_services",
    # "time_since_last_service",
]

df = df[features + ["event_occurred"]].copy()

df.rename(columns={"component_age": "duration"}, inplace=True)

cph = CoxPHFitter()
cph.fit(df, duration_col="duration", event_col="event_occurred")

joblib.dump(cph, "cox_model.pkl")
joblib.dump(label_encoders, "cox_label_encoders.pkl")
print("Cox model trained and saved")

print(df["event_occurred"].value_counts(normalize=True))
