import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from airflow.operators.python import PythonOperator
from mlflow.pyfunc import PythonModel
from sklearn.model_selection import train_test_split

import mlflow
from airflow import DAG
from mlops.config import MODEL_CONFIG
from mlops.processors.churn import ChurnProcessor

logger = logging.getLogger(__name__)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

DATA_PATH = Path(os.environ["MLOPS_DATA_PATH"])
MODEL_PATH = Path(os.environ["MLOPS_MODEL_PATH"])
MLFLOW_URI = os.environ["MLOPS_MLFLOW_URI"]


class ChurnPredictionModel(PythonModel):
    def __init__(self, model):
        self.model = model

    def predict(self, context, model_input, params=None):  # type: ignore
        return self.model.predict(model_input)


def load_data(**context):
    # Load the dataset
    dataset = pd.read_parquet(DATA_PATH)
    logger.info("Read parquet from: %s", DATA_PATH.as_posix())

    # Split the dataset into train and test sets
    X = dataset.drop(columns=[MODEL_CONFIG["models"]["churn"]["target"]])
    y = dataset[MODEL_CONFIG["models"]["churn"]["target"]]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=MODEL_CONFIG["models"]["churn"]["test_size"],
        random_state=MODEL_CONFIG["models"]["churn"]["random_seed"],
    )
    logger.info("Tran-test split done")

    # Push data to XCom
    logger.info("Pushing data to XCom")
    context["task_instance"].xcom_push(key="X_train", value=X_train.to_dict())  # type: ignore
    context["task_instance"].xcom_push(key="X_test", value=X_test.to_dict())  # type: ignore
    context["task_instance"].xcom_push(key="y_train", value=y_train.to_list())  # type: ignore
    context["task_instance"].xcom_push(key="y_test", value=y_test.to_list())  # type: ignore


def train_model(**context):
    # Pull data from XCom
    task_instance = context["task_instance"]
    X_train = pd.DataFrame(task_instance.xcom_pull(key="X_train"))
    y_train = pd.Series(task_instance.xcom_pull(key="y_train"))
    logger.info("Data loaded successfully from XCom")

    # Train model
    model = ChurnProcessor().train(X_train, y_train)
    logger.info("Model trained successfully")

    # Store the trained model temporarily
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    model.dump(metrics={}, model_path=MODEL_PATH.as_posix())
    logger.info("Model stored without metrics at: %s", MODEL_PATH.as_posix())


def evaluate_model(**context):
    """Evaluate the model and compute metrics"""
    # Get test data from XCom
    task_instance = context["task_instance"]
    X_test = pd.DataFrame(task_instance.xcom_pull(key="X_test"))
    y_test = pd.Series(task_instance.xcom_pull(key="y_test"))

    # Load the trained model
    model = ChurnProcessor.load(MODEL_PATH.as_posix())
    logger.info("Model loaded from: %s", MODEL_PATH.as_posix())

    # Compute metrics
    metrics = model.compute_metrics(X_test, y_test)
    logger.info("Metrics computed: %s", metrics)

    # Save final model with metrics
    model.dump(metrics=metrics, model_path=MODEL_PATH.as_posix())
    logger.info("Model stored with metrics at: %s", MODEL_PATH.as_posix())

    # Push metrics to XCom
    context["task_instance"].xcom_push(key="metrics", value=metrics)
    logger.info("Metrics pushed to XCom")


def mlflow_register_model(**context):
    # Pull metrics from XCom
    task_instance = context["task_instance"]
    metrics = task_instance.xcom_pull(key="metrics")

    # Set the experiment
    mlflow.set_tracking_uri(MLFLOW_URI)
    mlflow.set_experiment("churn-prediction-loyola")

    # Load the model
    model = ChurnProcessor.load(MODEL_PATH.as_posix())

    # Log the model
    with mlflow.start_run():
        mlflow.log_params(MODEL_CONFIG["models"]["churn"])
        mlflow.log_metrics(metrics)
        mlflow.pyfunc.log_model(
            "model",
            python_model=ChurnPredictionModel(model),
            artifacts={"model": MODEL_PATH.as_posix()},
        )
        run_id = mlflow.active_run().info.run_id

    # Push run_id to XCom
    context["task_instance"].xcom_push(key="run_id", value=run_id)
    logger.info("Run ID pushed to XCom: %s", run_id)


def mlflow_load_model(**context):
    # Pull test data from XCom
    task_instance = context["task_instance"]
    run_id = task_instance.xcom_pull(key="run_id")

    # Load the model
    mlflow.set_tracking_uri(MLFLOW_URI)
    model = mlflow.pyfunc.load_model(f"runs:/{run_id}/model")

    # Make predictions
    X_test = pd.DataFrame(task_instance.xcom_pull(key="X_test")).values
    predictions = model.predict(X_test)
    logger.info("Predictions: %s", predictions)

    # Push predictions to XCom
    context["task_instance"].xcom_push(key="predictions", value=predictions[0].tolist())
    context["task_instance"].xcom_push(key="scores", value=predictions[1].tolist())
    logger.info("Predictions pushed to XCom")


with DAG(
    "churn_training_pipeline",
    default_args=default_args,
    description="A pipeline to train and evaluate the churn model",
    schedule_interval=timedelta(days=7),  # Weekly training
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ml", "churn"],
) as dag:
    # Task 1: Load and split data
    load_data_task = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
    )

    # Task 2: Train model
    train_model_task = PythonOperator(
        task_id="train_model",
        python_callable=train_model,
    )

    # Task 3: Evaluate model
    evaluate_model_task = PythonOperator(
        task_id="evaluate_model",
        python_callable=evaluate_model,
    )

    mlflow_register_model_task = PythonOperator(
        task_id="mlflow_register_model",
        python_callable=mlflow_register_model,
    )

    mlflow_load_model_task = PythonOperator(
        task_id="mlflow_load_model",
        python_callable=mlflow_load_model,
    )

    # Define task dependencies
    load_data_task >> train_model_task >> evaluate_model_task >> mlflow_register_model_task >> mlflow_load_model_task
