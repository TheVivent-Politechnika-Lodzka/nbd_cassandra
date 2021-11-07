from cassandra.cluster import Cluster
from cassandra.query import dict_factory
import random
import string
from datetime import datetime

cluster = Cluster(['172.18.02', '172.18.0.3'])
session = cluster.connect('nbd')
session.row_factory = dict_factory


def get_session():
    return session


def get_id(size=23, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def json_review_validation(json_review):

    review_id = get_id()
    business_id = json_review['business_id'] if 'business_id' in json_review else None
    if business_id is None:
        raise Exception('business_id is not set')
    user_id = json_review['user_id'] if 'user_id' in json_review else None
    if user_id is None:
        raise Exception('user_id is not set')
    stars = json_review['stars'] if 'stars' in json_review else 0
    text = json_review['text'] if 'text' in json_review else ""
    date = json_review['date'] if 'date' in json_review else datetime.now().strftime(
        '%d-%m-%Y %H:%M:%S')
    useful = json_review['useful'] if 'useful' in json_review else 0
    funny = json_review['funny'] if 'funny' in json_review else 0
    cool = json_review['cool'] if 'cool' in json_review else 0

    return review_id, business_id, user_id, stars, text, date, useful, funny, cool
