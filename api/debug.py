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


#SELECT * FROM articles WHERE article_id = daa8e01a-7080-11e9-bba6-08002757542a


objects = []
rows =session.execute("SELECT * FROM articles WHERE article_id="+"daa8e01a-7080-11e9-bba6-08002757542a")
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
