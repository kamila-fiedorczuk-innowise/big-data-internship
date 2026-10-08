from pathlib import Path

from src.db_connection import Connection
from src.json_read import JsonReader

DATA_DIR = Path(__file__).parent / "data"

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