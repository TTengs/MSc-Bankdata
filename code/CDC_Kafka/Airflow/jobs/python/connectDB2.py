from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder \
    .appName("DB2 JDBC Example") \
    .config("spark.driver.extraClassPath", "/spark/jars/db2jcc4.jar:/spark/jars/db2jcc-db2jcc4.jar") \
    .getOrCreate()

# JDBC URL
url = "jdbc:db2://ibmdb2:25010/testdb"

# JDBC properties
properties = {
    "user": "db2inst1",
    "password": "passw0rd",
    "driver": "com.ibm.db2.jcc.DB2Driver"
}

# Table name
table = "EMPLOYEES"

# Read data from DB2 table into a Spark DataFrame
df = spark.read.jdbc(url=url, table=table, properties=properties)

# Show the DataFrame
df.show()

# Stop the SparkSession
spark.stop()
