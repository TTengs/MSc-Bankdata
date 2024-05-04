import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

dag = DAG(
    dag_id = "spring_batch_test",
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

run_jar_task= BashOperator(
  task_id = 'runjar',
  dag = dag,
  bash_command = 'java -jar $AIRFLOW_HOME/jobs/SpringBatchJars/springDemo-0.0.1-SNAPSHOT.jar' #--spring.datasource.url=jdbc:db2://ibmdb2:25010/testdb --spring.datasource.username=db2inst1 --spring.datasource.password=passw0rd --spring.datasource.driver-class-name=com.ibm.db2.jcc.DB2Driver --spring.batch.jdbc.initialize-schema=always'
)

end = PythonOperator(
    task_id="end",
    python_callable = lambda: print("Jobs completed successfully"),
    dag=dag
)

start >> run_jar_task >> end