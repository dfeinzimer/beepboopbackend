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


article_ID = "c5404c8c-707a-11e9-bba6-08002757542a"
rows = session.execute("DELETE FROM articles WHERE article_id="+str(article_ID))
