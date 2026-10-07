-- create table rooms

CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- create table students

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birthday DATE NOT NULL,
    sex CHAR(1) NOT NULL,
    room_id INTEGER NOT NULL REFERENCES rooms(id)
);

-- create view for 2 and 3 query

CREATE OR REPLACE VIEW student_age AS
SELECT
    id,
    room_id,
    birthday,
    CAST(EXTRACT(YEAR FROM age(CURRENT_DATE, birthday)) AS int) AS age_years
FROM students;
