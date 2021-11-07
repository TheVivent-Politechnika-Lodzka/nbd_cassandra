from cassandra.cluster import Cluster
from cassandra.query import dict_factory
import random
import string

cluster = Cluster(['172.18.02', '172.18.0.3'])
session = cluster.connect('nbd')
session.row_factory = dict_factory


def get_session():
    return session


def get_id(size=23, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
