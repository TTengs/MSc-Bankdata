import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator

dag = DAG(
    dag_id = "triggerSparkTask",
    default_args = {
        "owner": "thten19",
        "start_date": airflow.utils.dates.days_ago(1)
    },
    schedule_interval = "@daily"
)

trigger = PythonOperator(
    task_id="triggerSpark",
    python_callable = lambda: print("Triggering Spark job..."),
    dag=dag
)

trigger