from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("run-pyspark-code").getOrCreate()


def etl(calls_df, customers_df):
    summary_df = calls_df.groupBy("date").agg(
        F.countDistinct("cust_id").alias("num_customers"),
        F.sum("duration").alias("total_duration"),
    )
    result_df = summary_df.select("date", "num_customers", "total_duration")
    return result_df
