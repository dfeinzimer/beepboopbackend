# https://www.tutorialspoint.com/flask/flask_sqlite.htm

import sqlite3

conn = sqlite3.connect('database_master.db')
print("Opened database successfully");

conn.execute('CREATE TABLE `users`\
    ( `user_id`	INTEGER NOT NULL UNIQUE, \
    `email`	TEXT NOT NULL UNIQUE, \
    `pass_hash`	INTEGER NOT NULL,\
    `display_name`	TEXT NOT NULL UNIQUE,\
    PRIMARY KEY(`user_id`));')

print("Table created successfully");
conn.close()
