import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

dag = DAG(
    dag_id = "db2_read",
    default_args = {
        "owner": "thten19",
        "start_date": airflow.utils.dates.days_ago(1)
    },
    schedule_interval = "@daily"
)

start = PythonOperator(
    task_id="start",
    python_callable = lambda: print("Jobs started"),
    dag=dag
)

db2_job = SparkSubmitOperator(
    task_id="db2_job",
    conn_id="spark-conn",
    driver_class_path="/spark_jars/db2jcc4.jar,/spark_jars/db2jcc-db2jcc4.jar",
    jars="/spark_jars/db2jcc4.jar,/spark_jars/db2jcc-db2jcc4.jar",
    application="jobs/python/connectDB2.py",
    dag=dag
)

end = PythonOperator(
    task_id="end",
    python_callable = lambda: print("Jobs completed successfully"),
    dag=dag
)

start >> db2_job >> end