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
        'Article title 1',
        'Article content 1',
        'Article headline 1',
        'David Feinzimer',
        '5/6/2019',
        'dfeinzimer',
        '5/6/2019'
    );"""
)
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
        'Article title 2',
        'Article content 2',
        'Article headline 2',
        'David Feinzimer',
        '5/6/2019',
        'dfeinzimer',
        '5/6/2019'
    );"""
)
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
        'Article title 3',
        'Article content 3',
        'Article headline 3',
        'David Feinzimer',
        '5/6/2019',
        'dfeinzimer',
        '5/6/2019'
    );"""
)
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
        'Article title 4',
        'Article content 4',
        'Article headline 4',
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
        'Article comment 1',
        '5/6/2019',
        'dfeinzimer'
    );"""
)
session.execute(
    """INSERT INTO comments (
        comment_id,
        article_url,
        comment,
        comment_date,
        user_display_name
    ) VALUES (
        uuid(),
        'articles/2',
        'Article comment 2',
        '5/6/2019',
        'dfeinzimer'
    );"""
)
session.execute(
    """INSERT INTO comments (
        comment_id,
        article_url,
        comment,
        comment_date,
        user_display_name
    ) VALUES (
        uuid(),
        'articles/2',
        'Article comment 3',
        '5/6/2019',
        'dfeinzimer'
    );"""
)
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
        'Article comment 4',
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
session.execute(
    """INSERT INTO tags (
        tag_id,
        tag,
        url
    ) VALUES (
        uuid(),
        'myTag2',
        'articles/2'
    );"""
)
session.execute(
    """INSERT INTO tags (
        tag_id,
        tag,
        url
    ) VALUES (
        uuid(),
        'myTag3',
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
        'user1',
        'user1@gmail.com'
    );"""
)
session.execute(
    """INSERT INTO users (
        user_id,
        display_name,
        email
    ) VALUES (
        uuid(),
        'user2',
        'user2@gmail.com'
    );"""
)
session.execute(
    """INSERT INTO users (
        user_id,
        display_name,
        email
    ) VALUES (
        uuid(),
        'user3',
        'user3@gmail.com'
    );"""
)
session.execute(
    """INSERT INTO users (
        user_id,
        display_name,
        email
    ) VALUES (
        uuid(),
        'user4',
        'user4@gmail.com'
    );"""
)
