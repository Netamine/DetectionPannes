import mlflow

def init_mlflow():
    mlflow.set_tracking_uri("mlruns")
    mlflow.set_experiment("lightgbm_experiment")

def log_params_and_metrics(params, metrics):
    mlflow.log_params(params)
    mlflow.log_metrics(metrics)

def log_model(model, model_name="lightgbm_model"):
    mlflow.lightgbm.log_model(model, artifact_path=f"data/models/{model_name}")
