#!/bin/bash

# Exec into the db2 container
docker exec ibmdb2 bash

# Switch to the db2inst1 user
echo "Switching to db2inst1 user"
su - db2inst1

# Connect to the testdb database and run the SQL script
echo "Connecting to testdb"
db2 connect to testdb

echo "Running SQL script"
db2 -tvf /home/db2inst1/config/db2.sql

echo "Verifying the table was created"
db2 "SELECT * FROM EMPLOYEES"