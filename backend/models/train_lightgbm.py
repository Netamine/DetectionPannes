import mlflow
import mlflow.lightgbm
import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from backend.utils.data_processing import load_data
from mlflow_config import init_mlflow, log_model

# Initialiser MLflow
init_mlflow()

# Charger les données
df = load_data("data/processed/MetroPT3_miniature.csv")

X = df.drop(columns=["target"])
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

params = {
    "objective": "regression",
    "metric": "rmse",
    "boosting_type": "gbdt",
    "num_leaves": 31,
    "learning_rate": 0.05,
    "feature_fraction": 0.9
}

with mlflow.start_run():
    mlflow.log_params(params)
    train_data = lgb.Dataset(X_train, label=y_train)
    valid_data = lgb.Dataset(X_test, label=y_test)

    model = lgb.train(params, train_data, valid_sets=[valid_data], num_boost_round=100, early_stopping_rounds=10)

    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    mlflow.log_metric("rmse", rmse)

    log_model(model)
    print(f"Modèle enregistré avec RMSE : {rmse:.4f}")
