import json
from random import seed
from threading import current_thread
from typing import Counter
from cas_tools import get_session, get_id
from flask import Flask, jsonify
from flask import request

# config
PAGE_SIZE = 2


app = Flask(__name__)


@app.route('/reviews', methods=['GET'])
def get_reviews():
    """
    Get all reviews
    """
    page = int(request.args.get('page', 1))
    session = get_session()
    reviews = session.execute('SELECT * FROM reviews_by_review_id')
    current_reviews = []
    counter = 0
    for review in reviews:
        counter += 1
        if counter < PAGE_SIZE * (page - 1):
            continue
        if counter > PAGE_SIZE * page:
            break
        current_reviews.append(review)
    return jsonify(current_reviews)


@app.route('/review/<string:review_id>', methods=['GET'])
def get_review(review_id):
    """
    Get a specific review
    """
    session = get_session()
    review = session.execute(
        f'SELECT * FROM reviews_by_review_id WHERE review_id = \'{review_id}\'')

    return jsonify(review.one())


# example of json request with httpie
# echo '{"business_id": "test", "user_id": "test", "text": "trochę tekstu", "stars": 5}' | http PUT http://localhost:5000/review

@app.route('/review', methods=['PUT'])
def create_review():
    """
    Create a new review
    """
    data = request.get_json()

    session = get_session()
    stmt = session.prepare("\
        INSERT INTO reviews_by_review_id (review_id, business_id, user_id, text, stars)\
        VALUES (?,?,?,?,?)\
    ")
    id = get_id()
    session.execute(
        stmt, [id, data["business_id"], data["user_id"], data["text"], data["stars"]])

    return jsonify({'status': 'ok', 'review_id': id})


@app.route('/review/<string:review_id>', methods=['POST'])
def update_review(review_id):
    """
    Update a review
    """
    data = request.get_json()

    session = get_session()
    stmt = session.prepare("\
        UPDATE reviews_by_review_id SET text = ?, stars = ? WHERE review_id = ?\
    ")
    session.execute(stmt, [data["text"], data["stars"], review_id])

    return jsonify({'status': 'ok', 'review_id': review_id})


@app.route('/review/<string:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Delete a review
    """
    session = get_session()
    stmt = session.prepare("\
        DELETE FROM reviews_by_review_id WHERE review_id = ?\
    ")
    session.execute(stmt, [review_id])

    return jsonify({'status': 'ok', 'review_id': review_id})


app.run(debug=True)
