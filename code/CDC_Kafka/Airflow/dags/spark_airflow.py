import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator
from airflow.operators.bash import BashOperator
from kafka import KafkaProducer
import json
from datetime import timedelta, datetime
from utils import on_failure_callback_dag, on_success_callback_dag, on_failure_callback_task, on_success_callback_task, on_execute_callback_task, on_sla_miss_callback_task

dag = DAG(
    dag_id = "test_SLA",
    on_failure_callback = on_failure_callback_dag,
    on_success_callback = on_success_callback_dag,
    sla_miss_callback = on_sla_miss_callback_task,
    default_args = {
        "owner": "thten19",
        "start_date": airflow.utils.dates.days_ago(1),
        "retries": 0,
        "on_failure_callback": on_failure_callback_task,
        "on_success_callback": on_success_callback_task,
        "on_execute_callback": on_execute_callback_task
    },
    schedule_interval = "@daily"
)

start = PythonOperator(
    task_id="start",
    python_callable = lambda: print("Jobs started"),
    dag=dag
)

word_count_job = SparkSubmitOperator(
    task_id="word_count_job",
    conn_id="spark-conn",
    application="jobs/python/wordCountJob.py",
    dag=dag
)

sleeper = BashOperator(
    task_id="sleeper",
    bash_command = 'sleep 30',
    dag=dag,
    sla=timedelta(seconds=10)
)

end = PythonOperator(
    task_id="end",
    python_callable = lambda: print("Jobs completed successfully"),
    dag=dag
)

start >> word_count_job >> end