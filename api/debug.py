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


#content = request.get_json()
new_id = uuid.uuid1()
new_tag = "My tag"
new_url = "articles/8f7acc30-707a-11e9-bba6-08002757542a"

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
        new_id,
        new_tag,
        new_url
    )
)
resp = json.dumps({"tag_id":str(new_id)})
