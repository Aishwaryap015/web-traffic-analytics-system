CREATE TABLE web_traffic (
    user_id INTEGER,
    session_id INTEGER,
    page TEXT,
    action TEXT,
    timestamp TEXT,
    source TEXT
);
SELECT name FROM sqlite_master WHERE type='table';
