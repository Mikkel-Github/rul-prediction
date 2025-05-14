import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
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
