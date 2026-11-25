from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("run-pyspark-code").getOrCreate()


def etl(input_df):
    high_views = F.col("view_count") > 1_000_000
    recent_release = F.col("release_year") >= 2024 - 5
    result_df = input_df.filter(high_views & recent_release)
    return result_df
