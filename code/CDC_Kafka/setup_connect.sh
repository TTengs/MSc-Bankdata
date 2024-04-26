#!/bin/bash
COLOR_GREEN='\033[0;32m'
NO_COLOR='\033[0m'

echo $COLOR_GREEN

echo "Create connector for db2"

echo $NO_COLOR

curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d @cdc/register-db2.json

echo $COLOR_GREEN

echo "Create connector for ibm mq"

echo $NO_COLOR

curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d @cdc/ibmmq_connector.json