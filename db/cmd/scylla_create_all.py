'''#############################################################################
Setup Cassandra, connect to a cluster and keyspace.
#############################################################################'''
from cassandra.cluster import Cluster
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
session.set_keyspace('beepboopbackend')



'''#############################################################################
Create an articles table
#############################################################################'''
session.execute(
    """CREATE TABLE IF NOT EXISTS articles(
        article_id int PRIMARY KEY,
        title text,
        content text,
        headline text,
        author text,
        article_date text,
        user_display_name text,
        last_modified text
    )"""
)



'''
conn = sqlite3.connect('../db/comments.db')
print("Opened comments.db successfully");
conn.execute('CREATE TABLE IF NOT EXISTS `comments`\
  (`comment_id`   INTEGER PRIMARY KEY AUTOINCREMENT,\
   `user_display_name`      TEXT NOT NULL,\
   `comment`      TEXT NOT NULL,\
   `article_url` TEXT NOT NULL,\
   `comment_date` TEXT NOT NULL);'
)
conn.execute('CREATE INDEX commentURL_idx ON comments(article_url);')
conn.close()
print("comments table created successfully",'\n');



conn = sqlite3.connect('../db/tags.db')
print("Opened tags.db successfully");
conn.execute('CREATE TABLE IF NOT EXISTS tags\
  (`tag_id` INTEGER PRIMARY KEY AUTOINCREMENT,\
   `tag`    TEXT NOT NULL,\
   `url`    TEXT);')
conn.execute('CREATE INDEX tag_idx ON tags(tag);')
conn.execute('CREATE INDEX url_idx ON tags(url);')
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
conn.execute('CREATE INDEX email_idx ON users(email);')
conn.close()
print("users table created successfully",'\n');
'''
