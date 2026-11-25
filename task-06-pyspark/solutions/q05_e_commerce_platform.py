from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("run-pyspark-code").getOrCreate()


def etl(products_df, orders_df):
    joined_df = products_df.join(orders_df, on="product_id", how="inner")
    summary_df = joined_df.groupBy("category").agg(
        F.avg("price").alias("avg_price"),
        F.count("order_id").alias("total_orders_count"),
    )
    return summary_df
