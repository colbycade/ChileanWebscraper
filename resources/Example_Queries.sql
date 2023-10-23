-- Total entries by letter 
SELECT IFNULL(letter, 'Total') as Letter, COUNT(*) as "Total Entries"
FROM (
    SELECT 
        CASE 
            WHEN UPPER(LEFT(entry_name, 1)) = 'Ñ' THEN 'N'  -- Prevents Ñ from appearing in results (the website doesn't distinguish)
            ELSE UPPER(LEFT(entry_name, 1))
        END as letter
    FROM entries
) subquery
GROUP BY letter
WITH ROLLUP;


-- See number of entries, contributors, and definitions
SELECT 
  (SELECT COUNT(*) FROM users) as 'Total Contributors',
  (SELECT COUNT(*) FROM entries) as 'Total Entries',
  (SELECT COUNT(*) FROM definitions) as 'Total Definitions';
  

-- See all definitions for a specific word/phrase
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

-- Average time since upload for all definitions
SELECT ROUND(AVG(time_in_days / 365), 2) 
AS "Avg Time in Years Since Upload" 
FROM definitions;

-- Oldest contributions
SELECT e.entry_name as Entry, d.definition_text as "Definition", d.example_text as Examples, 
d.synonyms as Synonyms, d.votes as Votes, d.time_since_upload as "Time Since Upload", u.username as Username
FROM definitions d
JOIN entries e ON d.entry_id = e.entry_id
JOIN users u ON d.user_id = u.user_id
ORDER BY d.time_in_days DESC;


-- Oldest users
SELECT u.username as Username, d_uniq.time_since_upload as "Time since first contribution"
FROM (
    SELECT user_id, MAX(time_in_days) as max_time
    FROM definitions
    GROUP BY user_id
) get_max  -- Finds the max time in days since upload for each user
JOIN (
    SELECT DISTINCT user_id, time_in_days, time_since_upload
    FROM definitions
) d_uniq ON d_uniq.user_id = get_max.user_id AND d_uniq.time_in_days = get_max.max_time
	-- The website only gives time since upload by the largest unit of time applicable (e.g., years), so we estimate with time_in_days in order to sort.
	-- This means if the user posted over a year ago, for example, all posts in the same year will have the same time_since_upload (and estimated time_in_days).
JOIN users u ON d_uniq.user_id = u.user_id
ORDER BY get_max.max_time DESC;


-- Most popular definitions
SELECT e.entry_name as 'Entry', d.definition_text as 'Definition', d.example_text as Examples, 
d.synonyms as Synonyms, CONCAT(d.time_since_upload, ' ago') as "Date Uploaded", d.votes as Votes
FROM definitions d
JOIN entries e ON d.entry_id = e.entry_id
ORDER BY d.votes DESC
LIMIT 50;


-- Definitions uploaded within the last year
SELECT e.entry_name as Entry, d.definition_text as "Definition", d.example_text as Examples, 
d.synonyms as Synonyms, d.votes as Votes, d.time_since_upload as "Time Since Upload", u.username as Username
FROM definitions d
JOIN entries e ON d.entry_id = e.entry_id
JOIN users u ON d.user_id = u.user_id
WHERE d.time_in_days < 365
ORDER BY d.time_in_days ASC;


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

