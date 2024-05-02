package com.airscholar.spark;

import scala.Tuple2;

import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.sql.SparkSession;

import java.util.Arrays;
import java.util.List;
import java.util.regex.Pattern;

public class WordCountJob {
	private static final Pattern SPACE = Pattern.compile(" ");

	public static void main(String[] args) throws Exception {

		SparkSession spark = SparkSession
		.builder()
		.appName("JavaWordCount")
		.getOrCreate();

		System.out.println("SparkSession created");

		spark.stop();
	}
}
