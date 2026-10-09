from pathlib import Path

from src.db_connection import Connection
from src.json_read import JsonReader
from src.sql_file_runner import SqlFileRunner
from src.data_loader import DataLoader
from src.query_runner import QueryRunner
from src.json_write import JsonWriter

DATA_DIR = Path(__file__).parent / "data"
SQL_DIR = Path(__file__).parent / "sql"
OUTPUT_DIR = Path(__file__).parent / "output"

if __name__ == "__main__":
    rooms_path = DATA_DIR / "rooms.json"
    rooms = JsonReader(rooms_path).read()
    students_path = DATA_DIR / "students.json"
    students = JsonReader(students_path).read()

    with Connection() as conn:
        print(f"Database: {conn.info.dbname} connected")

        # SCHEMA CREATION
        schema = SqlFileRunner(SQL_DIR / "schema.sql", conn)
        schema.create_sql()
        print("Schema Created")

        # DATA LOADER
        loader = DataLoader(conn)
        loader.load(rooms, students)
        print("Data was Loaded")

        # INDEX CREATION
        sql_index = SqlFileRunner(SQL_DIR / "indexes.sql", conn)
        sql_index.create_sql()
        print("SQL Indexes Created")

        # QUERIES
        runner = QueryRunner(conn, SQL_DIR)
        results = runner.run_all()
        print("Queries executed")

        # WRITE RESULTS
        writer = JsonWriter(OUTPUT_DIR / "query_results.json")
        output_path = writer.write(results)

        print(f"Saved: {output_path}")