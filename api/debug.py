#!/usr/bin/python3

import json
import uuid

'''#############################################################################
Setup Cassandra, connect to a cluster and keyspace.
#############################################################################'''
from cassandra.cluster import Cluster
from cassandra import ReadTimeout
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
session.set_keyspace('beepboopbackend')


'''#############################################################################
This file serves as a place to run  Scylla/Cassandra Python sytanx tests.
Add and run tests below.
#############################################################################'''

url = "articles/1"
print("new url",url)
rows = session.execute("SELECT article_url FROM comments;")
count = 0
objects = []
result = {}
for row in rows:
    result = {}
    if row.article_url == url:
        count = count + 1
result["count"] = count
objects.append(result)
print (json.dumps(objects))
