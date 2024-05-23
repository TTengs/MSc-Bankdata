"""
### DAG continuously listening to a Kafka topic for a specific message

This DAG will always run and asynchronously monitor a Kafka topic for a message 
which causes the funtion supplied to the `apply_function` parameter to return a value.
If a value is returned by the `apply_function`, the `event_triggered_function` is 
executed. Afterwards the task will go into a deferred state again. 
"""

from airflow.decorators import dag
from pendulum import datetime
from airflow.providers.apache.kafka.sensors.kafka import (
    AwaitMessageTriggerFunctionSensor,
)
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import json
import uuid

KAFKA_TOPIC = "AIRFLOW_SPARK_TRIGGER"


def listen_function(message):
    if message:
        return True


def event_triggered_function(event, **context):
    "Kicks off a downstream DAG with conf and waits for its completion."

    # use the TriggerDagRunOperator (TDRO) to kick off a downstream DAG
    TriggerDagRunOperator(
        trigger_dag_id="triggerSparkTask",
        task_id=f"triggered_downstream_dag_{uuid.uuid4()}",
        wait_for_completion=False,  # wait for downstream DAG completion
        poke_interval=5,
    ).execute(context)

    print("Trigger spark job to process the data...")


@dag(
    start_date=datetime(2023, 4, 1),
    schedule="@continuous",
    max_active_runs=1,
    catchup=False,
    render_template_as_native_obj=True,
)
def listen_for_Spark_trigger():
    listen_for_mq_event = AwaitMessageTriggerFunctionSensor(
        task_id="listen_for_spark_trigger",
        kafka_config_id="kafka_default",
        topics=[KAFKA_TOPIC],
        # the apply function will be used from within the triggerer, this is
        # why it needs to be a dot notation string
        apply_function="ibmmq_listener.listen_function",
        poll_interval=5,
        poll_timeout=1,
        event_triggered_function=event_triggered_function,
    )

listen_for_Spark_trigger()