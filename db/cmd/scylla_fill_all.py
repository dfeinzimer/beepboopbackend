import datetime
import hashlib
import random
import uuid

'''#############################################################################
The number of entries to add in each table.
#############################################################################'''
num_articles = 10
num_comments = 10
num_tags = 10
num_users = 10

new_user_ids = []
new_article_ids = []


'''#############################################################################
Setup Cassandra, connect to a cluster and keyspace.
#############################################################################'''
from cassandra.cluster import Cluster
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
session.set_keyspace('beepboopbackend')


'''#############################################################################
Fill the users table
#############################################################################'''
for x in range(0,num_users):
    newid = uuid.uuid1()
    new_user_ids.append(newid)
    password = "password"+str(x)
    pass_hash = hashlib.md5(password.encode())
    session.execute(
        """
        INSERT INTO users (
            user_id,
            email,
            display_name,
            pass_hash
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            newid,
            "user"+str(x)+"@email.com",
            "user"+str(x),
            str(pass_hash.hexdigest())
        )
    )
print("Created new users:")
for x in new_user_ids:
    print("\t",x)


'''#############################################################################
Fill the articles table
#############################################################################'''
for x in range(0,num_articles):
    newid = uuid.uuid1()
    new_article_ids.append(newid)
    session.execute(
        """
        INSERT INTO articles (
            article_id,
            title,
            content,
            headline,
            author,
            article_date,
            user_display_name,
            last_modified
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            newid,
            "Article title "+str(x),
            "Article content "+str(x),
            "Article headline "+str(x),
            'Anonymous',
            str(datetime.date.today()),
            "user"+str(x),
            str(datetime.date.today())
        )
    )
print("Created new articles:")
for x in new_user_ids:
    print("\t",x)


'''#############################################################################
Fill the comments table
#############################################################################'''
for x in range(0,num_comments):
    newid = uuid.uuid1()
    session.execute(
        """
        INSERT INTO comments (
            comment_id,
            article_url,
            comment,
            comment_date,
            user_display_name
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            newid,
            "articles/"+str(random.choice(new_article_ids)),
            "Article comment "+str(x),
            str(datetime.date.today()),
            "user"+str(x)
        )
    )


'''#############################################################################
Fill the tags table
#############################################################################'''
for x in range(0,num_tags):
    newid = uuid.uuid1()
    session.execute(
        """
        INSERT INTO tags (
            tag_id,
            tag,
            url
        )
        VALUES (%s, %s, %s)
        """,
        (
            newid,
            "myTag"+str(x),
            "articles/"+str(random.choice(new_article_ids))
        )
    )
