-- 	List of rooms and the number of students in each of them

SELECT
	r.id,
	COUNT(s.room_id) AS number_of_students	
FROM rooms AS r
LEFT JOIN students AS s
ON r.id = s.room_id
GROUP BY r.id
ORDER BY r.id;

-- 	5 rooms with the smallest average age of students

-- create view once - to use it in 2 queries
CREATE VIEW student_age AS
SELECT
    *,
    CAST(EXTRACT(YEAR FROM age(CURRENT_DATE, birthday)) AS int) AS age_years
FROM students;


SELECT
room_id,
AVG(age_years)
FROM student_age
GROUP BY room_id
ORDER BY AVG(age_years)
LIMIT 5;


-- 5 rooms with the largest difference in the age of students

SELECT
room_id,
MAX(age_years) - MIN(age_years) AS age_diffrence
FROM student_age
GROUP BY room_id
ORDER BY age_diffrence DESC
LIMIT 5;

-- List of rooms where different-sex students live

SELECT
room_id,
COUNT(DISTINCT(sex)) AS sex_number
FROM students
GROUP BY room_id
HAVING COUNT(DISTINCT(sex)) > 1