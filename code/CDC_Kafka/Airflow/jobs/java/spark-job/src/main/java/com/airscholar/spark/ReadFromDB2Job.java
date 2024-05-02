import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

public class DB2JDBCExample {
    public static void main(String[] args) {
        // Create a SparkSession
        SparkSession spark = SparkSession.builder()
                .appName("DB2 JDBC Example")
                .getOrCreate();

        // JDBC URL
        String url = "jdbc:db2://ibmdb2:50000/testdb";

        // JDBC properties
        java.util.Properties properties = new java.util.Properties();
        properties.setProperty("user", "db2inst1");
        properties.setProperty("password", "passw0rd");
        properties.setProperty("driver", "com.ibm.db2.jcc.DB2Driver");

        // Table name
        String table = "EMPLOYEES";

        // Read data from DB2 table into a Spark DataFrame
        Dataset<Row> df = spark.read().jdbc(url, table, properties);

        // Show the DataFrame
        df.show();

        // Stop the SparkSession
        spark.stop();
    }
}
