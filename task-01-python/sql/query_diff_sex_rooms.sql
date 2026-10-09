-- List of rooms where different-sex students live

SELECT
room_id,
COUNT(DISTINCT sex) AS sex_number
FROM students
GROUP BY room_id
HAVING COUNT(DISTINCT sex) > 1
ORDER BY room_id ASC;