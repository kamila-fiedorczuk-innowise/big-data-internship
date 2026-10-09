# This class is for schema creation and for adding indexes

from pathlib import Path
import psycopg


class SqlFileRunner:
    def __init__(self, path, conn):
        self.path = Path(path)
        self.conn = conn

    def read_sql_file(self):
        schema = self.path.read_text(encoding="utf-8")
        return schema

    def create_sql(self):
        sql_query = self.read_sql_file()
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql_query)
                self.conn.commit()
        except psycopg.Error:
            self.conn.rollback()
            raise