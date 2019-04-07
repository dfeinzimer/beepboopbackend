CREATE TABLE IF NOT EXISTS comments
  (comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
   user_id text NOT NULL,
   comment text NOT NULL,
   comment_date text NOT NULL);
