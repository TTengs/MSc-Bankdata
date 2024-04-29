FROM apache/airflow:2.7.3-python3.11

USER root
RUN apt-get update && \
    apt-get install -y gcc python3-dev openjdk-11-jdk && \
    apt-get clean

#Set environment variables JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
RUN export JAVA_HOME

#For mac I think
#ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-arm64

USER airflow

RUN pip install apache-airflow apache-airflow-providers-apache-spark pyspark confluent-kafka airflow-provider-kafka apache-airflow-providers-apache-kafka