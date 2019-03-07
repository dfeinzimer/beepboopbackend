CREATE TABLE IF NOT EXISTS  users
            (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
             email TEXT NOT NULL UNIQUE,
             display_name TEXT NOT NULL,
             pass_hash TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS articles
            (article_id INTEGER PRIMARY KEY AUTOINCREMENT, 
             title text NOT NULL,
             content text NOT NULL, 
             headline text, 
             author text NOT NULL,
             article_date text NOT NULL, 
             last_modified text NOT NULL);

CREATE TABLE IF NOT EXISTS comments
            (comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
             user_id text NOT NULL,
             comment text NOT NULL,
             comment_date text NOT NULL);
