import os

from airflow.sdk import Asset

# Values from environment variables (set in .env, passed to containers by docker-compose)
DATA_DIR = os.environ["DATA_DIR"]
PROCESSED_DIR = os.environ["PROCESSED_DIR"]
INPUT_FILENAME = os.environ["INPUT_FILENAME"]

# Paths built from the values above
INPUT_FILE = os.path.join(DATA_DIR, INPUT_FILENAME)
CLEAN_REVIEWS_FILE = os.path.join(PROCESSED_DIR, "03_clean_content.csv")

# Asset shared by the processing (producer) and loading (consumer) DAGs
CLEAN_REVIEWS_ASSET = Asset(
    name="tiktok_reviews_clean",
    uri=f"file://{CLEAN_REVIEWS_FILE}",
)

# Airflow connections and MongoDB target
FS_CONN_ID = "fs_data"
MONGO_CONN_ID = "mongo_tiktok"
MONGO_DB = "tiktok"
MONGO_COLLECTION = "reviews"
