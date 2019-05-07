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
