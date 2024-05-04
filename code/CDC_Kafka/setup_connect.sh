#!/bin/bash

#echo "Create connector for db2"

#curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d @cdc/register-db2.json

echo "Create source connector for ibm mq"

curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d @cdc/ibmmq_source_connector.json

echo "Create sink connector for ibm mq"

curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d @cdc/ibmmq_sink_connector.json