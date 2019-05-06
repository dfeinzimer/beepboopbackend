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
        article_id uuid PRIMARY KEY,
        title text,
        content text,
        headline text,
        author text,
        article_date text,
        user_display_name text,
        last_modified text
    )"""
)



'''#############################################################################
Create an comments table
#############################################################################'''
session.execute(
    """CREATE TABLE IF NOT EXISTS comments(
        comment_id int PRIMARY KEY,
        user_display_name text,
        comment text,
        article_url text,
        comment_date text
    )"""
)



'''#############################################################################
Create a tags table
#############################################################################'''
session.execute(
    """CREATE TABLE IF NOT EXISTS tags(
        tag_id int PRIMARY KEY,
        tag text,
        url text
    )"""
)



'''#############################################################################
Create a users table
#############################################################################'''
session.execute(
    """CREATE TABLE IF NOT EXISTS users(
        user_id int PRIMARY KEY,
        email text,
        pass_hash text,
        display_name text
    )"""
)
