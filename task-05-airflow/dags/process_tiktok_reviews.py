import os
from datetime import datetime

from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.sdk import dag, task, task_group

DATA_DIR = "/opt/airflow/data"
INPUT_FILENAME = "tiktok_google_play_reviews.csv"
INPUT_FILE = os.path.join(DATA_DIR, INPUT_FILENAME)
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")


@dag(
    dag_id="process_tiktok_reviews",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["tiktok"],
)
def process_tiktok_reviews():
    wait_for_file = FileSensor(
        task_id="wait_for_file",
        fs_conn_id="fs_data",
        filepath=INPUT_FILENAME,
        poke_interval=30,
        timeout=60 * 60,
        mode="reschedule",
    )

    @task.branch
    def check_if_empty():
        size = os.path.getsize(INPUT_FILE)
        if size > 0:
            return "process_data.replace_nulls"
        return "log_empty_file"

    log_empty_file = BashOperator(
        task_id="log_empty_file",
        bash_command="echo file is empty",
    )

    @task_group(group_id="process_data")
    def process_data():
        @task
        def replace_nulls(input_path):
            import pandas as pd

            os.makedirs(PROCESSED_DIR, exist_ok=True)
            df = pd.read_csv(input_path)
            df = df.fillna("-")
            output_path = os.path.join(PROCESSED_DIR, "01_no_nulls.csv")
            df.to_csv(output_path, index=False)
            return output_path

        @task
        def sort_by_date(input_path):
            import pandas as pd

            df = pd.read_csv(input_path)
            df["at"] = pd.to_datetime(df["at"])
            df = df.sort_values("at")
            output_path = os.path.join(PROCESSED_DIR, "02_sorted.csv")
            df.to_csv(output_path, index=False)
            return output_path

        @task
        def clean_content(input_path):
            import pandas as pd

            df = pd.read_csv(input_path)
            df["content"] = df["content"].str.replace(
                r"[^\w\s.,!?'\":;()\-]", "", regex=True
            )
            df["content"] = df["content"].str.strip().replace("", "-")
            output_path = os.path.join(PROCESSED_DIR, "03_clean_content.csv")
            df.to_csv(output_path, index=False)
            return output_path

        clean_content(sort_by_date(replace_nulls(INPUT_FILE)))

    wait_for_file >> check_if_empty() >> [log_empty_file, process_data()]


process_tiktok_reviews()
