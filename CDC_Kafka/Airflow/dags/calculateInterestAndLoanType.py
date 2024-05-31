import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.kafka.operators.consume import ConsumeFromTopicOperator
from airflow.providers.apache.kafka.triggers.await_message import AwaitMessageTrigger
import json
import time
from datetime import timedelta, datetime
from airflow.models import DagRun
from airflow import settings
from utils import (
    on_failure_callback_dag, 
    on_success_callback_dag, 
    on_failure_callback_task, 
    on_success_callback_task, 
    on_execute_callback_task, 
    on_sla_miss_callback_task
)

dag = DAG(
    dag_id = "calculateInterestAndLoanType",
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

spring_job = BashOperator(
    task_id = 'calculate_interest_spring_job',
    dag = dag,
    bash_command = 'java -jar $AIRFLOW_HOME/jobs/SpringBatchJars/springDemo-0.0.1-SNAPSHOT.jar'
)

java_job = SparkSubmitOperator(
    task_id="calculate_loan_type_spark_job",
    conn_id="spark-conn",
    application="jobs/java/spark-job/target/spark-job-1.0-SNAPSHOT.jar",
    java_class="com.airscholar.spark.CalculateLoanTypeJob",
    driver_class_path="/spark_jars/db2jcc4.jar,/spark_jars/db2jcc-db2jcc4.jar",
    jars="/spark_jars/db2jcc4.jar,/spark_jars/db2jcc-db2jcc4.jar",
    dag=dag
)

end = PythonOperator(
    task_id="end",
    python_callable = lambda: print("Jobs completed successfully"),
    dag=dag
)

start >> spring_job >> java_job >> end