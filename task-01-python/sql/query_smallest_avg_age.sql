-- 	5 rooms with the smallest average age of students

SELECT room_id,
CAST(ROUND(AVG(age_years), 2) AS double precision) AS average_age
FROM student_age
GROUP BY room_id
ORDER BY average_age ASC, room_id ASC
LIMIT 5;