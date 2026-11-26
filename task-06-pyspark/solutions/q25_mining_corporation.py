from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("run-pyspark-code").getOrCreate()


def etl(mines, extraction):
    join_df = mines.join(extraction, mines["id"] == extraction["mine_id"], how="inner")
    summary_df = join_df.groupBy("location", "mineral").agg(
        F.sum("quantity").cast("double").alias("total_quantity")
    )
    result_df = summary_df.orderBy("location", "mineral")
    return result_df
