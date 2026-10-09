-- 	List of rooms and the number of students in each of them

SELECT
	r.id,
	COUNT(s.room_id) AS number_of_students	
FROM rooms AS r
LEFT JOIN students AS s
ON r.id = s.room_id
GROUP BY r.id
ORDER BY r.id;