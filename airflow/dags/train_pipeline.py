import logging
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from airflow.operators.python import PythonOperator
from sklearn.model_selection import train_test_split

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

DATA_PATH = Path("./data/churn/data.parquet")
MODEL_PATH = Path("./artifacts/models/churn/model.flm")


def load_data(**context):
    """Load the dataset and split it into train and test sets"""
    dataset = pd.read_parquet(DATA_PATH)
    logger.info("Read parquet from: %s", DATA_PATH.as_posix())

    X = dataset.drop(columns=[MODEL_CONFIG["models"]["churn"]["target"]])
    y = dataset[MODEL_CONFIG["models"]["churn"]["target"]]
    logger.info("X, y data loaded")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=MODEL_CONFIG["models"]["churn"]["test_size"],
        random_state=MODEL_CONFIG["models"]["churn"]["random_seed"],
    )
    logger.info("Tran-test split done")

    logger.info("Pushing data to XCom")
    context["task_instance"].xcom_push(key="X_train", value=X_train.to_dict())  # type: ignore
    context["task_instance"].xcom_push(key="X_test", value=X_test.to_dict())  # type: ignore
    context["task_instance"].xcom_push(key="y_train", value=y_train.to_list())  # type: ignore
    context["task_instance"].xcom_push(key="y_test", value=y_test.to_list())  # type: ignore


def train_model(**context):
    """Train the churn model"""
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


# Create the DAG
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

    # Define task dependencies
    load_data_task >> train_model_task >> evaluate_model_task
