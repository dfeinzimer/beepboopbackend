# https://www.tutorialspoint.com/flask/flask_sqlite.htm



import sqlite3



conn = sqlite3.connect('../db/articles.db')
print("Opened articles.db successfully");
conn.execute('CREATE TABLE IF NOT EXISTS `articles`\
  (`article_id` INTEGER PRIMARY KEY AUTOINCREMENT,\
   `title` text NOT NULL,\
   `content` text NOT NULL,\
   `headline` text,\
   `author` text NOT NULL,\
   `article_date` text NOT NULL,\
   `last_modified` text NOT NULL);'
)
conn.close()
print("articles table created successfully",'\n');



conn = sqlite3.connect('../db/comments.db')
print("Opened comments.db successfully");
conn.execute('CREATE TABLE IF NOT EXISTS `comments`\
  (`comment_id` INTEGER PRIMARY KEY AUTOINCREMENT,\
   `user_id text` NOT NULL,\
   `comment text` NOT NULL,\
   `comment_date` text NOT NULL);'
)
conn.close()
print("comments table created successfully",'\n');



conn = sqlite3.connect('../db/tags.db')
print("Opened tags.db successfully");
conn.execute('CREATE TABLE IF NOT EXISTS tags\
  (`tag_id` INTEGER PRIMARY KEY AUTOINCREMENT,\
   `tag` text NOT NULL,\
   `url` text);')
conn.close()
print("tags table created successfully",'\n');



conn = sqlite3.connect('../db/users.db')
print("Opened users.db successfully");
conn.execute('CREATE TABLE `users`\
    ( `user_id`	INTEGER NOT NULL UNIQUE, \
    `email`	TEXT NOT NULL UNIQUE, \
    `pass_hash`	INTEGER NOT NULL,\
    `display_name`	TEXT NOT NULL UNIQUE,\
    PRIMARY KEY(`user_id`));')
conn.close()
print("users table created successfully",'\n');
