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
comment_ID = "7bcb4cff-cfb7-478c-af2d-f6bde6c41d40"
session.execute("DELETE FROM comments WHERE comment_id="+str(comment_ID))
