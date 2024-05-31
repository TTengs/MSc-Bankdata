from kafka import KafkaProducer
import json
#The possible callback types
#https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/callbacks.html

def send_to_kafka(message, dag_id):
    producer = KafkaProducer(bootstrap_servers=['kafka:29092'])

    #Create kafka topic
    KAFKA_TOPIC = f"{dag_id}_state"

    producer.send(KAFKA_TOPIC, message.encode('utf-8'))
    producer.flush()
    producer.close()

def on_failure_callback_dag(context):
    dag_state_message(context)
    print(f"Dag run {dag_run.run_id} failed")

def on_success_callback_dag(context):
    dag_state_message(context)
    print(f"Dag run {dag_run.run_id} succeeded")

def on_failure_callback_task(context):
    task_state_message(context)
    print("Sending fail task state to Kafka")

def on_success_callback_task(context):
    task_state_message(context)
    print("Sending success task state to Kafka")

def on_execute_callback_task(context):
    task_state_message(context)
    print("Sending execute task state to Kafka")

def on_sla_miss_callback_task(dag, task_list, blocking_task_list, slas, blocking_tis):
    #Make custom SLA message
    print("Sending SLA miss task state to Kafka")
    task_sla_missed_message(dag, task_list, blocking_task_list, slas, blocking_tis)

def task_state_message(context):
    dag_id = context.get("dag").dag_id
    dag_run = context.get("dag_run")
    task_instance = context.get("task_instance")
    state = task_instance.state
    run_id = dag_run.run_id
    
    # Construct JSON message
    message = {
        "id": dag_id,
        "info": {
            "run_id": run_id,
            "task_id": task_instance.task_id,
            "state_date": task_instance.start_date,
            "end_date": task_instance.end_date,
            "state": state
        }
    }
    json_message = json.dumps(message, default=str)
    # Produce the message to a Kafka topic
    send_to_kafka(json_message, dag_id)

def dag_state_message(context):
    dag_id = context.get("dag").dag_id
    dag_run = context.get("dag_run")
    state = dag_run.state
    run_id = dag_run.run_id
    
    # Construct JSON message
    message = {
        "id": dag_id,
        "info": {
            "run_id": run_id,
            "state": state
        }
    }
    json_message = json.dumps(message, default=str)
    # Produce the message to a Kafka topic
    send_to_kafka(json_message, dag_id)

def task_sla_missed_message(dag, task_list, blocking_task_list, slas, blocking_tis):
    print("SLA is broken for the following dag: " + dag.dag_id)
    # Construct JSON message
    message = {
        "id": dag.dag_id,
        "info": {
            "dag": dag,
            "task_list": task_list,
            "blocking_task_list": blocking_task_list,
            "slas": slas,
            "blocking_tis": blocking_tis,
        }
    }
    json_message = json.dumps(message, default=str)
    # Produce the message to a Kafka topic
    send_to_kafka(json_message, dag.dag_id)