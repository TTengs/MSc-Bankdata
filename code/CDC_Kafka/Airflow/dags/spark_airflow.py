import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator
from kafka import KafkaProducer
import json

KAFKA_TOPIC = "sparking_simple_submit_state"

def prod_function(message):
    print("what")
    yield json.dumps(message)

def send_to_kafka(message):
    print("Sending message to Kafka")
    producer = KafkaProducer(bootstrap_servers=['kafka:29092'])

    producer.send(KAFKA_TOPIC, message.encode('utf-8'))
    producer.flush()
    producer.close()
    # producer = ProduceToTopicOperator(
    #     task_id="produce_to_kafka",
    #     kafka_config_id="kafka_default",
    #     poll_timeout=10,
    #     topic=KAFKA_TOPIC,
    #     producer_function=prod_function,
    #     producer_function_args=message,
    # )

def on_failure_callback_dag(context):
    dag_run = context.get("dag_run")
    print(f"Dag run {dag_run.run_id} failed")

def on_failure_callback_task(context):
    dag_run = context.get("dag_run")
    task_instance = context.get("task_instance")
    #Produce the error to a Kafka topic
    print(f"Error: {task_instance.task_id} failed for dag run {dag_run.run_id}")

def on_success_callback_task(context):
    dag_id = context.get("dag").dag_id
    dag_run = context.get("dag_run")
    task_instance = context.get("task_instance")
    state = task_instance.state
    run_id = dag_run.run_id
    #Produce the error to a Kafka topic
    message = json.dumps ({"dag_id": dag_id, "task_id": task_instance.task_id, "state": state, "run_id": run_id})
    send_to_kafka(message)
    print(f"TEST DAG: {dag_id}, Task: {task_instance.task_id}, State: {state}, succeeded for dag run {dag_run.run_id}")

dag = DAG(
    dag_id = "sparking_simple_submit",
    on_failure_callback = on_failure_callback_dag,
    default_args = {
        "owner": "thten19",
        "start_date": airflow.utils.dates.days_ago(1),
        "on_failure_callback": on_failure_callback_task,
        "on_success_callback": on_success_callback_task
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

# java_job = SparkSubmitOperator(
#     task_id="java_job",
#     conn_id="spark-conn",
#     application="jobs/java/spark-job/target/spark-job-1.0-SNAPSHOT.jar",
#     java_class="com.airscholar.spark.WordCountJob",
#     dag=dag
# )

end = PythonOperator(
    task_id="end",
    python_callable = lambda: print("Jobs completed successfully"),
    dag=dag
)

start >> word_count_job >> end