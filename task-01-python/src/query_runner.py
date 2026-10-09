from pathlib import Path

from psycopg.rows import dict_row


class QueryRunner:
    def __init__(self, conn, queries_dir):
        self.conn = conn
        self.queries_dir = Path(queries_dir)

    def _read_sql_file(self, file_name):
        file_path = self.queries_dir / file_name
        return file_path.read_text(encoding="utf-8")

    def _run_query(self, file_name):
        query = self._read_sql_file(file_name)
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query)
            return cur.fetchall()

    def query_rooms_student_count(self):
        return self._run_query("query_rooms_student_count.sql")

    def query_smallest_avg_age(self):
        return self._run_query("query_smallest_avg_age.sql")

    def query_largest_diff_age(self):
        return self._run_query("query_largest_diff_age.sql")

    def query_diff_sex_rooms(self):
        return self._run_query("query_diff_sex_rooms.sql")

    def run_all(self):
        return {
            "query_rooms_student_count": self.query_rooms_student_count(),
            "query_smallest_avg_age": self.query_smallest_avg_age(),
            "query_largest_diff_age": self.query_largest_diff_age(),
            "query_diff_sex_rooms": self.query_diff_sex_rooms(),
        }