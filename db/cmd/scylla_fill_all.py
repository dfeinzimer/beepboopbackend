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
        'The best article title ever',
        'Great article content 2',
        'A good headline 2',
        'David Feinzimer',
        '5/6/2019',
        'dfeinzimer',
        '5/6/2019'
    );"""
)



'''#############################################################################
Fill the comments table
#############################################################################'''
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
        'What a great article',
        '5/6/2019',
        'dfeinzimer'
    );"""
)



'''#############################################################################
Fill the tags table
#############################################################################'''
session.execute(
    """INSERT INTO tags (
        tag_id,
        tag,
        url
    ) VALUES (
        uuid(),
        'myTag1',
        'articles/1'
    );"""
)



'''#############################################################################
Fill the users table
#############################################################################'''
session.execute(
    """INSERT INTO users (
        user_id,
        display_name,
        email
    ) VALUES (
        uuid(),
        'user3',
        'user1@gmail.com'
    );"""
)
