from cassandra.cluster import Cluster

cluster = Cluster(['172.17.0.2'])

session = cluster.connect('beepboopbackend')
