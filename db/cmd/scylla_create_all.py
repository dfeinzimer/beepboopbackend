'''#############################################################################
Setup Cassandra, connect to a cluster and keyspace.
#############################################################################'''
from cassandra.cluster import Cluster
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()

KEYSPACE = "beepboopbackend"


session.execute("""
    CREATE KEYSPACE IF NOT EXISTS %s
    WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
    """ % KEYSPACE)


session.set_keyspace(KEYSPACE)

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
        comment_id uuid PRIMARY KEY,
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
        tag_id uuid PRIMARY KEY,
        tag text,
        url text
    )"""
)



'''#############################################################################
Create a users table
#############################################################################'''
session.execute(
    """CREATE TABLE IF NOT EXISTS users(
        user_id uuid,
        email text,
        pass_hash text,
        display_name text, 
        PRIMARY KEY (email, pass_hash)
    )"""
)
