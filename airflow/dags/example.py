import datetime

from airflow.operators.python import PythonOperator

from airflow import DAG

today = datetime.datetime.now()
start_date = today - datetime.timedelta(days=1)

# Configuration
default_args = {
    "owner": "airflow",
    "description": "Simple example DAG - MLOps Course",
    "depends_on_past": False,
    "start_date": start_date,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=10),
}

with DAG("simple-example", default_args=default_args, schedule_interval=datetime.timedelta(days=1)):
    task_1 = PythonOperator(
        task_id="task_1",
        python_callable=lambda: print("Welcome to the MLOps Course"),  # noqa: T201
    )

    task_2 = PythonOperator(
        task_id="task_2",
        python_callable=lambda: print("This is one simple example DAG"),  # noqa: T201
    )

    task_3 = PythonOperator(
        task_id="task_3",
        python_callable=lambda: print("This is another simple example DAG"),  # noqa: T201
    )

    task_4 = PythonOperator(
        task_id="task_4",
        python_callable=lambda: print("See you in the next lesson"),  # noqa: T201
    )

    task_1 >> [task_2, task_3] >> task_4
