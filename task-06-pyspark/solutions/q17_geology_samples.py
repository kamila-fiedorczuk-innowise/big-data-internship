from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("run-pyspark-code").getOrCreate()


def etl(input_df):
    with_age_df = input_df.withColumn(
        "age", F.regexp_extract(F.col("description"), r"(\d+)", 1)
    )
    return with_age_df
