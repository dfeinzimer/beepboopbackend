CREATE TABLE IF NOT EXISTS articles
            (article_id INTEGER PRIMARY KEY AUTOINCREMENT, 
             title text NOT NULL,
             content text NOT NULL, 
             headline text, 
             author text NOT NULL,
             article_date text NOT NULL, 
             last_modified text NOT NULL);

