'''#############################################################################
The number of entries to add in each table.
#############################################################################'''
num_articles = 10
num_comments = 10
num_tags = 10
num_users = 10


'''#############################################################################
Setup Cassandra, connect to a cluster and keyspace.
#############################################################################'''
from cassandra.cluster import Cluster
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
session.set_keyspace('beepboopbackend')


'''#############################################################################
Fill the articles table
#############################################################################'''
for x in range(0,num_articles):
    session.execute(
        """INSERT INTO articles (
            article_id,
            title,
            content,
            headline,
            author,
            article_date,
            user_display_name,
            last_modified
        ) VALUES (
            uuid(),
            'Article title """+str(x)+"""',
            'Article content """+str(x)+"""',
            'Article headline """+str(x)+"""',
            'Anonymous',
            '5/6/2019',
            'user"""+str(x)+"""',
            '5/6/2019'
        );"""
    )


'''#############################################################################
Fill the comments table
#############################################################################'''
for x in range(0,num_comments):
    session.execute(
        """INSERT INTO comments (
            comment_id,
            article_url,
            comment,
            comment_date,
            user_display_name
        ) VALUES (
            uuid(),
            'articles/1',
            'Article comment """+str(x)+"""',
            '5/6/2019',
            'user"""+str(x)+"""'
        );"""
    )


'''#############################################################################
Fill the tags table
#############################################################################'''
for x in range(0,num_tags):
    session.execute(
        """INSERT INTO tags (
            tag_id,
            tag,
            url
        ) VALUES (
            uuid(),
            'myTag"""+str(x)+"""',
            'articles/1'
        );"""
    )


'''#############################################################################
Fill the users table
#############################################################################'''
for x in range(0,num_users):
    session.execute(
        """INSERT INTO users (
            user_id,
            display_name,
            email
        ) VALUES (
            uuid(),
            'user"""+str(x)+"""',
            'user"""+str(x)+"""@gmail.com'
        );"""
    )
