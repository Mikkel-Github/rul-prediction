import ast

import optuna
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBRegressor

df = pd.read_csv("../data-generator/for_tests_TRAINING.csv")
df = df.dropna(subset=["RUL"])
X = df.drop(
    columns=["RUL", "machine_id", "prev_failures", "is_failure", "lifecycle_id"]
)
y = df["RUL"]


categorical_features = ["component", "machine_type", "event_type_encoded"]
numerical_features = [
    "component_age",
    "num_services_since_install",
]

preprocessor = ColumnTransformer(
    [
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", StandardScaler(), numerical_features),
    ]
)


def random_forest(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 300),
        "max_depth": trial.suggest_int("max_depth", 4, 20),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 10),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 5),
        "random_state": 42,
    }
    model = RandomForestRegressor(**params)

    pipeline = Pipeline([("preprocessor", preprocessor), ("regressor", model)])

    score = cross_val_score(
        pipeline, X, y, cv=5, scoring="neg_root_mean_squared_error"
    ).mean()
    return -score


def xgboost(trial):
    params = {
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 1.0),
        "gamma": trial.suggest_float("gamma", 0, 3),
        "max_depth": trial.suggest_int("max_depth", 1, 12),
        "min_child_weight": trial.suggest_float("min_child_weight", 1, 3),
        # "max_delta_step": trial.suggest_float("max_delta_step", 0, 6),
        "subsample": trial.suggest_float("subsample", 0.1, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0, 1),
        "colsample_bylevel": trial.suggest_float("colsample_bylevel", 0, 1),
        "colsample_bynode": trial.suggest_float("colsample_bynode", 0, 1),
        "lambda": trial.suggest_float("lambda", 0, 6),
        "alpha": trial.suggest_float("alpha", 0, 6),
        "max_leaves": trial.suggest_int("max_leaves", 0, 16),
        "max_bin": trial.suggest_int("max_bin", 128, 512),
        "n_estimators": trial.suggest_int("n_estimators", 50, 300),
        "reg_alpha": trial.suggest_float("reg_alpha", 0, 3),
        "reg_lambda": trial.suggest_float("reg_lambda", 0, 3),
        "random_state": 42,
    }
    model = XGBRegressor(objective="reg:squarederror", tree_method="hist", **params)

    pipeline = Pipeline([("preprocessor", preprocessor), ("regressor", model)])

    score = cross_val_score(
        pipeline, X, y, cv=5, scoring="neg_root_mean_squared_error"
    ).mean()
    return -score


def lightgbm(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 300),
        "max_depth": trial.suggest_int("max_depth", 3, 12),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
        "num_leaves": trial.suggest_int("num_leaves", 15, 150),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
        "random_state": 42,
    }
    model = LGBMRegressor(**params)

    pipeline = Pipeline([("preprocessor", preprocessor), ("regressor", model)])

    score = cross_val_score(
        pipeline, X, y, cv=5, scoring="neg_root_mean_squared_error"
    ).mean()
    return -score


def machine_learning(trial):
    layer_choices = [
        "(64,)",
        "(64, 32)",
        "(64, 64)",
        "(128,)",
        "(100, 50)",
        "(128, 64)",
    ]
    layer_str = trial.suggest_categorical("hidden_layer_sizes", layer_choices)
    hidden_layers = ast.literal_eval(layer_str)

    alpha = trial.suggest_float("alpha", 1e-5, 1e-2, log=True)
    learning_rate_init = trial.suggest_float("learning_rate_init", 1e-4, 1e-2, log=True)
    max_iter = trial.suggest_int("max_iter", 200, 1000)

    model = MLPRegressor(
        activation="relu",
        solver="adam",
        hidden_layer_sizes=hidden_layers,
        alpha=alpha,
        learning_rate_init=learning_rate_init,
        max_iter=max_iter,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=5,
        random_state=42,
        verbose=False,
    )

    pipeline = Pipeline([("preprocessor", preprocessor), ("regressor", model)])

    score = cross_val_score(
        pipeline, X, y, cv=5, scoring="neg_root_mean_squared_error"
    ).mean()
    return -score


study = optuna.create_study(direction="minimize")
# study.optimize(random_forest, n_trials=50)
study.optimize(xgboost, n_trials=100)
# study.optimize(lightgbm, n_trials=50)
# study.optimize(machine_learning, n_trials=50)

print(f"Best RMSE: {study.best_value:.4f}")
print("Best hyperparameters:", study.best_params)
