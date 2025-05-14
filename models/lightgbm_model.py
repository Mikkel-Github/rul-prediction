import joblib
import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split
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
    columns=["RUL", "machine_type", "component_age", "lifecycle_id", "is_failure"]
)
y = df["RUL"]

# LightGBM model
model = lgb.LGBMRegressor(
    objective="regression",
    n_estimators=297,
    max_depth=3,
    learning_rate=0.29776431900950884,
    num_leaves=150,
    subsample=0.8391750944956501,
    colsample_bytree=0.9944041997612525,
    random_state=42,
    n_jobs=-1,
)
model.fit(X, y)

joblib.dump((model, X.columns.tolist()), "lightgbm_model.pkl")
joblib.dump(label_encoders, "lightgbm_label_encoders.pkl")
print("LightGBM model trained and saved")


# importances = model.feature_importances_
#
# feature_importance_df = pd.DataFrame({"Feature": X.columns, "Importance": importances})
#
# feature_importance_df = feature_importance_df.sort_values(
#     by="Importance", ascending=False
# )
#
# print(feature_importance_df)
