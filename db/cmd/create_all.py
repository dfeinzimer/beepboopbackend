# https://www.tutorialspoint.com/flask/flask_sqlite.htm



import sqlite3



conn = sqlite3.connect('../db/articles.db')
print("Opened articles.db successfully");
conn.execute('CREATE TABLE IF NOT EXISTS `articles`\
  (`article_id`           INTEGER PRIMARY KEY AUTOINCREMENT,\
   `title`                TEXT NOT NULL,\
   `content`              TEXT NOT NULL,\
   `headline`             TEXT,\
   `author`               TEXT NOT NULL,\
   `article_date`         TEXT NOT NULL,\
   `user_display_name`    TEXT NOT NULL,\
   `last_modified`        TEXT NOT NULL);'
)
conn.close()
print("articles table created successfully",'\n');



conn = sqlite3.connect('../db/comments.db')
print("Opened comments.db successfully");
conn.execute('CREATE TABLE IF NOT EXISTS `comments`\
  (`comment_id`   INTEGER PRIMARY KEY AUTOINCREMENT,\
   `user_display_name`      TEXT NOT NULL,\
   `comment`      TEXT NOT NULL,\
   `comment_date` TEXT NOT NULL);'
)
conn.close()
print("comments table created successfully",'\n');



conn = sqlite3.connect('../db/tags.db')
print("Opened tags.db successfully");
conn.execute('CREATE TABLE IF NOT EXISTS tags\
  (`tag_id` INTEGER PRIMARY KEY AUTOINCREMENT,\
   `tag`    TEXT NOT NULL,\
   `url`    TEXT);')
conn.close()
print("tags table created successfully",'\n');



conn = sqlite3.connect('../db/users.db')
print("Opened users.db successfully");
conn.execute('CREATE TABLE `users`\
    ( `user_id`	      INTEGER NOT NULL UNIQUE, \
      `email`	      TEXT NOT NULL UNIQUE, \
      `pass_hash`     TEXT NOT NULL,\
      `display_name`  TEXT NOT NULL UNIQUE,\
    PRIMARY KEY(`user_id`));')
conn.close()
print("users table created successfully",'\n');
