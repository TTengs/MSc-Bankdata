#!/bin/bash
COLOR_GREEN='\033[0;32m'
NO_COLOR='\033[0m'

echo $COLOR_GREEN

echo "Create connector for postgres"

echo $NO_COLOR

curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8093/connectors/ -d @cdc/postgres_connector.json