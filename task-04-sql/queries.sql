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
WITH movie_top_rank AS (
    SELECT
        a.actor_id,
        a.first_name,
        a.last_name,
        COUNT(*) AS num_of_movies,
        DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS movie_rank
    FROM actor AS a
    INNER JOIN film_actor AS fa
        ON a.actor_id = fa.actor_id
    INNER JOIN film_category AS fc
        ON fa.film_id = fc.film_id
    INNER JOIN category AS c
        ON fc.category_id = c.category_id
    WHERE c.name = 'Children'
    GROUP BY a.actor_id, a.first_name, a.last_name
)

SELECT
    actor_id,
    first_name,
    last_name,
    num_of_movies
FROM movie_top_rank
WHERE movie_rank <= 3
ORDER BY num_of_movies DESC;

-- 6. Cities with number of active and inactive customers,
--    sorted by inactive descending
SELECT
    cit.city,
    SUM(CASE WHEN c.active = 1 THEN 1 ELSE 0 END) AS active_customers,
    SUM(CASE WHEN c.active = 0 THEN 1 ELSE 0 END) AS inactive_customers
FROM customer AS c
INNER JOIN address AS a
    ON c.address_id = a.address_id
INNER JOIN city AS cit
    ON a.city_id = cit.city_id
GROUP BY cit.city, cit.city_id
ORDER BY inactive_customers DESC;


-- 7. Category with the most total rental hours in cities starting with "a"
--    and in cities containing "-" (one query)
