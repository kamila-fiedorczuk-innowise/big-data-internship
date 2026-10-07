import os

import psycopg
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

conn = psycopg.connect(host=host, port=port, dbname=dbname, user=user, password=password)

cur = conn.cursor()
cur.execute("SELECT version();")
ver = cur.fetchone()
print(ver[0])

cur.close()
conn.close()
