-- Summary of totals
SELECT IFNULL(Letter, 'Total') as Letter, COUNT(*) as "Total Entries"
FROM (
    SELECT UPPER(LEFT(entry_name, 1)) as Letter
    FROM entries
) subquery
GROUP BY Letter
WITH ROLLUP;


-- See number of entries, contributors, and definitions
SELECT 
  (SELECT COUNT(*) FROM users) as 'Total Contributors',
  (SELECT COUNT(*) FROM entries) as 'Total Entries',
  (SELECT COUNT(*) FROM definitions) as 'Total Definitions';


-- List all definitions for a specific entry
SELECT d.* FROM definitions d
JOIN entries e ON d.entry_id = e.entry_id
WHERE e.entry_name = 'yapo';


-- Entries with most contributors
SELECT e.entry_name as Entry, COUNT(*) as "Number of Definitions"
FROM definitions d
JOIN entries e on d.entry_id = e.entry_id
GROUP BY e.entry_id
ORDER BY COUNT(*) DESC
LIMIT 20;


-- Most popular definitions
SELECT * FROM definitions
ORDER BY votes DESC
LIMIT 50;


-- Top contributors
SELECT u.username, COUNT(*) as num_contributions
FROM definitions d
JOIN users u on d.user_id = u.user_id
GROUP BY u.user_id
ORDER BY num_contributions DESC
LIMIT 50;


-- Average number of votes per definition
SELECT ROUND(AVG(votes),2) as average_votes FROM definitions;


-- Most popular entries
WITH RankedEntries AS (		-- Get all entries
    SELECT 
        e.entry_name, 
        SUM(d.votes) as total_votes,
        MAX(d.votes) as top_definition_votes
    FROM definitions d
    JOIN entries e ON d.entry_id = e.entry_id
    GROUP BY e.entry_id
),
TopDefinitions AS (		-- Filter to get only top definitions
    SELECT
        e.entry_id,
        e.entry_name,
        d.votes,
        d.definition_text
    FROM definitions d
    JOIN entries e ON d.entry_id = e.entry_id
    JOIN RankedEntries r ON e.entry_name = r.entry_name
    WHERE d.votes = r.top_definition_votes
)
SELECT 
    RANK() OVER (ORDER BY r.total_votes DESC) as Ranking, 
    r.entry_name as Entry, 
    r.total_votes as "Total Votes for Entry", 
    t.definition_text as "Top Definition",
    r.top_definition_votes as "Votes for Top Definition",
    CONCAT(ROUND((r.top_definition_votes / r.total_votes * 100), 2), '%') as "Percent of Total"
FROM RankedEntries r
LEFT JOIN TopDefinitions t ON r.entry_name = t.entry_name
ORDER BY r.total_votes DESC;

