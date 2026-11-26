from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("run-pyspark-code").getOrCreate()


def etl(input_df1, input_df2):
    all_customers_df = input_df1.unionByName(input_df2)
    return all_customers_df
