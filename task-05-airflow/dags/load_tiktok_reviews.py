from datetime import datetime

from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.sdk import dag, task
from pipeline_config import (
    CLEAN_REVIEWS_ASSET,
    CLEAN_REVIEWS_FILE,
    MONGO_COLLECTION,
    MONGO_CONN_ID,
    MONGO_DB,
)


@dag(
    dag_id="load_tiktok_reviews",
    schedule=[CLEAN_REVIEWS_ASSET],
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["tiktok"],
)
def load_tiktok_reviews():
    @task
    def load_to_mongo():
        import pandas as pd

        df = pd.read_csv(CLEAN_REVIEWS_FILE, keep_default_na=False)
        df["at"] = pd.to_datetime(df["at"])
        records = df.to_dict(orient="records")

        hook = MongoHook(mongo_conn_id=MONGO_CONN_ID)
        hook.delete_many(
            mongo_collection=MONGO_COLLECTION, filter_doc={}, mongo_db=MONGO_DB
        )
        hook.insert_many(
            mongo_collection=MONGO_COLLECTION, docs=records, mongo_db=MONGO_DB
        )
        print(f"Loaded {len(records)} documents into {MONGO_DB}.{MONGO_COLLECTION}")

    load_to_mongo()


load_tiktok_reviews()
