from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("run-pyspark-code").getOrCreate()


def etl(social_media):
    result_df = social_media.withColumn(
        "text", F.regexp_replace(F.col("text"), "Python", "PySpark")
    )
    return result_df
