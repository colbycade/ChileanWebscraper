SELECT IFNULL(Letter, 'Total') as Letter, COUNT(*) as Count
FROM (
    SELECT UPPER(LEFT(entry_name, 1)) as Letter
    FROM entries
) subquery
GROUP BY Letter
WITH ROLLUP;

SELECT * FROM users;