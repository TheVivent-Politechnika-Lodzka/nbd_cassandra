from cassandra.cluster import Cluster

cluster = Cluster(['172.18.02', '172.18.0.3'])
session = cluster.connect()

rows = session.execute('DESC KEYSPACES')
for keyspace_row in rows:
    print(keyspace_row.keyspace_name)