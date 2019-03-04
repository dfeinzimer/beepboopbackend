--DEV 1 SCHEMA
CREATE TABLE IF NOT EXISTS articles
            (article_id INTEGER PRIMARY KEY AUTOINCREMENT, 
             title text, 
             headline text, 
             author text NOT NULL,
             article_date text NOT NULL, 
             last_modified text NOT NULL);


CREATE TABLE IF NOT EXISTS  users
            (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
             email TEXT NOT NULL,
             display_name TEXT NOT NULL,
             pass_hash TEXT NOT NULL);