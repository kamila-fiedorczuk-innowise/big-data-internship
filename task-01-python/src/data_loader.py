import psycopg


class DataLoader:
    def __init__(self, conn):
        self.conn = conn

    def _insert_rooms(self, cur, rooms):
        sql = ("INSERT INTO rooms (id, name) VALUES (%(id)s, %(name)s)"
               " ON CONFLICT DO NOTHING;")
        cur.executemany(sql, rooms)

    def _insert_students(self, cur, students):
        sql = ("INSERT INTO students (id, name, birthday, sex, room_id) "
               "VALUES (%(id)s, %(name)s, %(birthday)s, %(sex)s, %(room)s)"
               " ON CONFLICT DO NOTHING;")
        cur.executemany(sql, students)

    def load(self, rooms, students):
        try:
            with self.conn.cursor() as cur:
                self._insert_rooms(cur, rooms)
                self._insert_students(cur, students)
                self.conn.commit()
        except psycopg.Error:
            self.conn.rollback()
            raise