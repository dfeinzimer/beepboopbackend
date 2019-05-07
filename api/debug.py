#!/usr/bin/python3

import json

'''#############################################################################
Setup Cassandra, connect to a cluster and keyspace.
#############################################################################'''
from cassandra.cluster import Cluster
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
session.set_keyspace('beepboopbackend')
'''#############################################################################
Older Cassandra implementation possibly no longer necessary
#############################################################################'''
#from flask_cassandra import CassandraCluster
#cassandra = CassandraCluster()
#app.config['CASSANDRA_NODES'] = ['172.17.0.2']


#    query = "SELECT * FROM articles"
#    resp = query_db(query)
#    result = jsonify(resp)
#    return result



objects = []
rows = session.execute('SELECT * FROM articles')
for row in rows:
    result = {}
    result["article_date"] = row.article_date
    result["author"] = row.author
    result["content"] = row.content
    result["headline"] = row.headline
    result["last_modified"] = row.last_modified
    result["title"] = row.title
    result["user_display_name"] = row.user_display_name
    objects.append(result)
print(objects)
print(json.dumps(objects))
