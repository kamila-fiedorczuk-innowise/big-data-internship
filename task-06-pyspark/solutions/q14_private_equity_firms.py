from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("run-pyspark-code").getOrCreate()


def etl(pe_firms, pe_funds, pe_investments):
    firms_funds_df = pe_firms.join(pe_funds, on="firm_id", how="outer")
    full_df = firms_funds_df.join(pe_investments, on="fund_id", how="outer")
    clean_df = full_df.dropna(how="all")
    return clean_df
