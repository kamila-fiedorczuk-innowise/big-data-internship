-- 5 rooms with the largest difference in the age of students

SELECT
room_id,
MAX(age_years) - MIN(age_years) AS age_difference
FROM student_age
GROUP BY room_id
ORDER BY age_difference DESC, room_id ASC
LIMIT 5;