-- Index for the average age and age difference queries.
-- Rows are sorted by room, and inside each room by birthday,
-- so all students of one room sit next to each other
-- and the database can read room and birthday from the index.
CREATE INDEX IF NOT EXISTS idx_students_room_id_birthday
    ON students (room_id, birthday);

-- Index for the mixed-sex rooms query.
-- Same idea: sorted by room, then by sex,
-- so the database can count different sexes per room from the index.
CREATE INDEX IF NOT EXISTS idx_students_room_id_sex
    ON students (room_id, sex);