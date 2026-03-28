-- Remove null users
DELETE FROM web_traffic
WHERE user_id IS NULL;

-- Remove invalid actions
DELETE FROM web_traffic
WHERE action NOT IN ('visit','view','add','purchase');

-- Remove NULL timestamps
DELETE FROM web_traffic WHERE timestamp IS NULL;

-- Remove duplicate sessions
DELETE FROM web_traffic
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM web_traffic
    GROUP BY user_id, session_id, timestamp
);

-- Standardize source names
UPDATE web_traffic
SET source = LOWER(source);