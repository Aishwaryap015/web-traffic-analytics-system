--------------------------------------------------
-- 1. TOTAL USERS (KPI)
--------------------------------------------------
SELECT COUNT(DISTINCT user_id) AS total_users
FROM web_traffic;

--------------------------------------------------
-- 2. TRAFFIC BY SOURCE (MARKETING PERFORMANCE)
--------------------------------------------------
SELECT source, COUNT(*) AS visits
FROM web_traffic
GROUP BY source
ORDER BY visits DESC;

--------------------------------------------------
-- 3. DAILY TRAFFIC TREND (GROWTH ANALYSIS)
--------------------------------------------------
SELECT DATE(timestamp) AS day, COUNT(*) AS visits
FROM web_traffic
GROUP BY day
ORDER BY day;

--------------------------------------------------
-- 4. FUNNEL ANALYSIS (USER DROP-OFF)
--------------------------------------------------
WITH funnel AS (
    SELECT session_id,
        MAX(CASE WHEN action = 'visit' THEN 1 ELSE 0 END) AS visit,
        MAX(CASE WHEN action = 'view' THEN 1 ELSE 0 END) AS view,
        MAX(CASE WHEN action = 'add' THEN 1 ELSE 0 END) AS add_to_cart,
        MAX(CASE WHEN action = 'purchase' THEN 1 ELSE 0 END) AS purchase
    FROM web_traffic
    GROUP BY session_id
)
SELECT 
    COUNT(*) AS total_sessions,
    SUM(view) AS viewed,
    SUM(add_to_cart) AS added_to_cart,
    SUM(purchase) AS purchased,
    (SUM(purchase) * 100.0 / COUNT(*)) AS conversion_rate
FROM funnel;

--------------------------------------------------
-- 5. OVERALL CONVERSION RATE
--------------------------------------------------
SELECT 
    COUNT(DISTINCT CASE WHEN action='purchase' THEN session_id END) * 1.0 /
    COUNT(DISTINCT session_id) AS conversion_rate
FROM web_traffic;

--------------------------------------------------
-- 6. SOURCE-WISE CONVERSION (MARKETING ROI)
--------------------------------------------------
SELECT source,
    COUNT(DISTINCT CASE WHEN action='purchase' THEN session_id END) * 1.0 /
    COUNT(DISTINCT session_id) AS conversion_rate
FROM web_traffic
GROUP BY source;

--------------------------------------------------
-- 7. USER JOURNEY (BEHAVIOR ANALYSIS)
--------------------------------------------------
SELECT user_id, session_id, GROUP_CONCAT(page, ' → ') AS journey
FROM web_traffic
GROUP BY user_id, session_id;

--------------------------------------------------
-- 8. USERS BY SOURCE (JOIN ANALYSIS)
--------------------------------------------------
SELECT u.country, w.source, COUNT(*) AS visits
FROM web_traffic w
JOIN users u ON w.user_id = u.user_id
GROUP BY u.country, w.source;

--------------------------------------------------
-- 9. TOP ACTIVE USERS
--------------------------------------------------
SELECT u.user_name, COUNT(w.session_id) AS sessions
FROM users u
JOIN web_traffic w ON u.user_id = w.user_id
GROUP BY u.user_name
ORDER BY sessions DESC;

--------------------------------------------------
-- 10. USER RETENTION (ENGAGEMENT)
--------------------------------------------------
SELECT user_id, COUNT(DISTINCT DATE(timestamp)) AS active_days
FROM web_traffic
GROUP BY user_id;

--------------------------------------------------
-- 11. ADVANCED: RUNNING TRAFFIC TREND (WINDOW FUNCTION)
--------------------------------------------------

SELECT 
    DATE(timestamp) AS day,
    COUNT(*) AS daily_visits,
    SUM(COUNT(*)) OVER (ORDER BY DATE(timestamp)) AS cumulative_visits
FROM web_traffic
GROUP BY day;

--------------------------------------------------
-- 12. FUNNEL ANALYSIS
--------------------------------------------------

SELECT page, COUNT(*) AS visits
FROM web_traffic
GROUP BY page
ORDER BY visits DESC; 

--------------------------------------------------
-- 13. CONVERSION RATE
--------------------------------------------------

SELECT 
    COUNT(CASE WHEN action = 'purchase' THEN 1 END) * 1.0 /
    COUNT(*) AS conversion_rate
FROM web_traffic;

--------------------------------------------------
-- 14. SESSION LENGTH
--------------------------------------------------

SELECT session_id, COUNT(*) AS steps
FROM web_traffic
GROUP BY session_id
ORDER BY steps DESC;

--------------------------------------------------
-- 15. USER RETENTION
--------------------------------------------------

SELECT user_id, COUNT(DISTINCT DATE(timestamp)) AS active_days
FROM web_traffic
GROUP BY user_id
ORDER BY active_days DESC;

--------------------------------------------------
-- 16. WINDOW FUNCTION
--------------------------------------------------

SELECT 
    DATE(timestamp) AS day,
    COUNT(*) AS daily_visits,
    SUM(COUNT(*)) OVER (ORDER BY DATE(timestamp)) AS cumulative_visits
FROM web_traffic
GROUP BY day;

.mode csv
.import data/users.csv users
