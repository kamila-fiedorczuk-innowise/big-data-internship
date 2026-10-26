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
SELECT
    a.actor_id,
    a.first_name AS actor_name,
    a.last_name AS actor_last_name,
    COUNT(r.rental_id) AS rental_count
FROM actor AS a
INNER JOIN film_actor AS fa
    ON a.actor_id = fa.actor_id
INNER JOIN inventory AS i
    ON fa.film_id = i.film_id
INNER JOIN rental AS r
    ON i.inventory_id = r.inventory_id
GROUP BY a.actor_id, a.first_name, a.last_name
ORDER BY COUNT(r.rental_id) DESC
LIMIT 10;

-- 3. Category of movies on which the most money was spent
SELECT
    c.name,
    SUM(p.amount) AS money_spent
FROM category AS c
INNER JOIN film_category AS fc
    ON c.category_id = fc.category_id
INNER JOIN inventory AS i
    ON fc.film_id = i.film_id
INNER JOIN rental AS r
    ON i.inventory_id = r.inventory_id
INNER JOIN payment AS p
    ON r.rental_id = p.rental_id
GROUP BY c.category_id, c.name
ORDER BY money_spent DESC
LIMIT 1;

-- 4. Movies that are not in the inventory (without IN)
SELECT f.title
FROM film AS f
LEFT JOIN inventory AS i
    ON f.film_id = i.film_id
WHERE i.film_id IS NULL
ORDER BY f.title;

-- 5. Top 3 actors with the most movies in "Children" category (ties included)


-- 6. Cities with number of active and inactive customers,
--    sorted by inactive descending


-- 7. Category with the most total rental hours in cities starting with "a"
--    and in cities containing "-" (one query)
