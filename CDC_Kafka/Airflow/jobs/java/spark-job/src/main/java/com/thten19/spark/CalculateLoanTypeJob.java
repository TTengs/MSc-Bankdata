package com.thten19.spark;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class CalculateLoanTypeJob {
    public static void main(String[] args) throws SQLException {
        // Create a SparkSession
        SparkSession spark = SparkSession.builder()
                .appName("Calculate Loan Type of Accounts")
                .getOrCreate();

        // JDBC URL
        String url = "jdbc:db2://ibmdb2:25010/testdb";

        // JDBC properties
        java.util.Properties properties = new java.util.Properties();
        properties.setProperty("user", "db2inst1");
        properties.setProperty("password", "passw0rd");
        properties.setProperty("driver", "com.ibm.db2.jcc.DB2Driver");
        properties.setProperty("isolationLevel", "NONE");
        //properties.setProperty("batchsize", 10);

        // Table name
        String account_table = "ACCOUNT";

        Dataset<Row> df;

        Connection connection = DriverManager.getConnection(url, properties);
        try {
            connection.setAutoCommit(false);

            // Read data from DB2 table into a Spark DataFrame
            df = spark.read().jdbc(url, account_table, properties);

            connection.commit();
        } catch (Exception e) {
            connection.rollback();
            throw e;
        } finally {
            connection.close();
        }

        // Calculate loan type score based on available balance
        Dataset<Row> loanTypeScore = df.withColumn("loan_type",
                org.apache.spark.sql.functions.when(
                        org.apache.spark.sql.functions.col("balance").lt(0), "D"
                ).when(
                        org.apache.spark.sql.functions.col("balance").between(0, 49999), "C"
                ).when(
                        org.apache.spark.sql.functions.col("balance").between(50000, 249999), "B"
                ).otherwise("A")
        );

        // Select only the account_id and loan_type columns
        Dataset<Row> accountLoanType = loanTypeScore.select("account_id", "loan_type");

        // Table name
        String account_loan_type_table = "ACCOUNT_LOAN_TYPE";

        // Write the result to the account_loan_type table
        accountLoanType.write()
                .mode("overwrite")
                .option("batchsize", 10)
                .jdbc(url, account_loan_type_table, properties);

        // Stop the SparkSession
        spark.stop();
    }
}
