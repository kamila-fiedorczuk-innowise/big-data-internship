import os
from datetime import datetime

from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.sdk import dag, task

DATA_DIR = "/opt/airflow/data"
INPUT_FILENAME = "tiktok_google_play_reviews.csv"
INPUT_FILE = os.path.join(DATA_DIR, INPUT_FILENAME)


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
            return "process_file"
        return "log_empty_file"

    log_empty_file = BashOperator(
        task_id="log_empty_file",
        bash_command="echo file is empty",
    )

    @task
    def process_file():
        print("File has data")

    wait_for_file >> check_if_empty() >> [log_empty_file, process_file()]


process_tiktok_reviews()
