import json
from pathlib import Path

from src.db_connection import Connection
from src.json_read import JsonReader
from src.sql_file_runner import SqlFileRunner
from src.data_loader import DataLoader
from src.query_runner import QueryRunner

DATA_DIR = Path(__file__).parent / "data"
SQL_DIR = Path(__file__).parent / "sql"

if __name__ == "__main__":

    # CONNECTION TEST
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT version();")
        print(cur.fetchone()[0])
    # END CONNECTION TEST

    # JSON READ TEST
    test_files = [
        DATA_DIR / "rooms.json",
        DATA_DIR / "students.json",
        DATA_DIR / "missing.json",
    ]

    for path in test_files:
        try:
            records = JsonReader(path).read()
            print(f"{path.name}: {len(records)} records")
        except (FileNotFoundError, ValueError) as e:
            print(f"ERROR: {e}")
    # END JSON READ TEST

    # SCHEMA CREATION TEST
    with Connection() as conn:
        print(f"Database: {conn.info.dbname}")

        schema = SqlFileRunner(SQL_DIR / "schema.sql", conn)
        schema.create_sql()
        schema.create_sql()
        print("create_schema() ran twice without errors")

        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM rooms;")
            print(f"rooms: {cur.fetchone()[0]} rows")

            cur.execute("SELECT COUNT(*) FROM students;")
            print(f"students: {cur.fetchone()[0]} rows")

            cur.execute("SELECT COUNT(*) FROM student_age;")
            print(f"student_age: {cur.fetchone()[0]} rows")
    # END SCHEMA CREATION TEST

    # DATA LOADER TEST
    with Connection() as conn:
        rooms = JsonReader(DATA_DIR / "rooms.json").read()
        students = JsonReader(DATA_DIR / "students.json").read()

        loader = DataLoader(conn)
        loader.load(rooms, students)
        loader.load(rooms, students)
        print("load() ran twice without errors")

        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM rooms;")
            print(f"rooms: {cur.fetchone()[0]} rows (expected {len(rooms)})")

            cur.execute("SELECT COUNT(*) FROM students;")
            print(f"students: {cur.fetchone()[0]} rows (expected {len(students)})")
    # END DATA LOADER TEST
    # QUERY RUNNER TEST
    with Connection() as conn:
        runner = QueryRunner(conn, SQL_DIR)
        results = runner.run_all()

        for name, rows in results.items():
            print(f"{name}: {len(rows)} rows")
            for key, value in rows[0].items():
                print(f"  {key}: {value!r} ({type(value).__name__})")

        print(json.dumps(results, indent=2)[:500])
    # END QUERY RUNNER TEST