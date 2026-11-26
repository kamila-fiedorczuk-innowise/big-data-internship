from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("run-pyspark-code").getOrCreate()


def etl(employees, payroll):
    emp_pay_df = employees.join(payroll, on="employee_id", how="inner")

    has_overtime = F.col("hours_worked") > 40
    overtime_pay = (
        40 * F.col("hourly_rate")
        + (F.col("hours_worked") - 40) * F.col("hourly_rate") * 1.5
    )
    regular_pay = F.col("hours_worked") * F.col("hourly_rate")

    pay_count_df = emp_pay_df.withColumn(
        "pay", F.when(has_overtime, overtime_pay).otherwise(regular_pay)
    )
    pay_float_df = pay_count_df.withColumn("pay", F.col("pay").cast("float"))
    result_df = pay_float_df.select("employee_id", "name", "position", "pay")
    return result_df
