from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("run-pyspark-code").getOrCreate()


def etl(movies_df):
    null_box_office_df = movies_df.filter(F.col("box_office_collection").isNull())
    return null_box_office_df
