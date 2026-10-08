#CONNECTION TEST

from src.db_connection import Connection

with Connection() as conn:
    cur = conn.cursor()
    cur.execute("SELECT version();")
    print(cur.fetchone()[0])

#END CONNECTION TEST