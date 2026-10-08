import os

import psycopg
from dotenv import load_dotenv


class Connection:
    def __init__(self):
        load_dotenv()
        self.conn = None
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.dbname = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        if None in (self.host, self.port, self.dbname, self.user, self.password):
            raise ValueError("Missing database settings in .env (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)")

    def connect(self):
        self.conn = psycopg.connect(host=self.host,
                                    port=self.port,
                                    dbname=self.dbname,
                                    user=self.user,
                                    password=self.password)
        return self.conn

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()