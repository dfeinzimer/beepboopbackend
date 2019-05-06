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
    )"""
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
    )"""
)
"""



'''#############################################################################
Fill the tags table
#############################################################################'''
conn = sqlite3.connect('../db/tags.db')
if(conn != None):
  print("Opened tags.db successfully");
  conn.execute("INSERT INTO tags VALUES(null,'apples','articles/1')")
  conn.execute("INSERT INTO tags VALUES(null,'bananas','articles/1')")
  conn.execute("INSERT INTO tags VALUES(null,'corn','articles/1')")
  conn.commit()
  conn.close()
  print("tags table filled successfully",'\n');
else:
  print("Cannot open tags.db")



'''#############################################################################
Fill the users table
#############################################################################'''
conn = sqlite3.connect('../db/users.db')
if(conn != None):
  print("Opened users.db successfully");                        #test@email.com
  conn.execute("INSERT INTO users VALUES(null,'test@email.com','93942e96f5acd83e2e047ad8fe03114d','dfeinzimer')")
  conn.commit()
  conn.close()
  print("users table filled successfully",'\n');
else:
  print("Cannot open users.db")
"""
