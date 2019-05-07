#!/usr/bin/python3

import json
import uuid

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



id = uuid.uuid1()
session.execute(
    """
    INSERT INTO articles (
        article_id,
        title, content,
        headline, author,
        article_date, last_modified, user_display_name
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """,
    (id,"My title", "My content",
    "My headline", "David Feinzimer",
    "5/6/2019","5/6/2019","dfeinzimer")
)
print("id type",type(id))
print("id",json.dumps({"article_id":str(id)}))
