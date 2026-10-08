from pathlib import Path
import psycopg


class SchemaCreation:
    def __init__(self, path, conn):
        self.path = Path(path)
        self.conn = conn

    def read_schema(self):
        schema = self.path.read_text(encoding="utf-8")
        return schema

    def create_schema(self):
        sql_query = self.read_schema()
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql_query)
                self.conn.commit()
        except psycopg.Error:
            self.conn.rollback()
            raise