'''#############################################################################
Setup Cassandra, connect to a cluster and keyspace.
#############################################################################'''
from cassandra.cluster import Cluster
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
session.set_keyspace('beepboopbackend')



connection  = sqlite3.connect("../db/articles.db")
cursor = connection.cursor()
dropTableStatement = "DROP TABLE articles"
cursor.execute(dropTableStatement)
connection.close()
print("articles table dropped",'\n')



connection  = sqlite3.connect("../db/comments.db")
cursor = connection.cursor()
dropTableStatement = "DROP TABLE comments"
cursor.execute(dropTableStatement)
connection.close()
print("comments table dropped",'\n')



connection  = sqlite3.connect("../db/tags.db")
cursor = connection.cursor()
dropTableStatement = "DROP TABLE tags"
cursor.execute(dropTableStatement)
connection.close()
print("tags table dropped",'\n')



connection  = sqlite3.connect("../db/users.db")
cursor = connection.cursor()
dropTableStatement = "DROP TABLE users"
cursor.execute(dropTableStatement)
connection.close()
print("users table dropped",'\n')
