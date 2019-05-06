'''#############################################################################
Setup Cassandra, connect to a cluster and keyspace.
#############################################################################'''
from cassandra.cluster import Cluster
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
session.set_keyspace('beepboopbackend')



'''#############################################################################
Drop the articles table
#############################################################################'''
session.execute(
    """DROP TABLE IF EXISTS articles"""
)
print("articles table dropped",'\n')



'''#############################################################################
Drop the comments table
#############################################################################'''
session.execute(
    """DROP TABLE IF EXISTS comments"""
)
print("comments table dropped",'\n')



'''#############################################################################
Drop the tags table
#############################################################################'''
session.execute(
    """DROP TABLE IF EXISTS tags"""
)
print("tags table dropped",'\n')



'''#############################################################################
Drop the users table
#############################################################################'''
session.execute(
    """DROP TABLE IF EXISTS users"""
)
print("users table dropped",'\n')
