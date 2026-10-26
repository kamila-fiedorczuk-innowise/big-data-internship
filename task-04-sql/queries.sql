-- 1. Number of movies in each category, sorted descending
SELECT
    c.name AS film_category_name,
    COUNT(fc.film_id) AS films_count
FROM film_category AS fc
INNER JOIN category AS c
    ON fc.category_id = c.category_id
GROUP BY fc.category_id, c.name
ORDER BY COUNT(fc.film_id) DESC;

-- 2. Top 10 actors whose movies were rented the most, sorted descending


-- 3. Category of movies on which the most money was spent


-- 4. Movies that are not in the inventory (without IN)


-- 5. Top 3 actors with the most movies in "Children" category (ties included)


-- 6. Cities with number of active and inactive customers,
--    sorted by inactive descending


-- 7. Category with the most total rental hours in cities starting with "a"
--    and in cities containing "-" (one query)
