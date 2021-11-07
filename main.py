from cas_tools import get_session, json_review_validation
from flask import Flask, jsonify
from flask import request

# example of json request with httpie
# echo '{"business_id": "test", "user_id": "test", "text": "trochę tekstu", "stars": 5, "useful": 4, "funny": 3, "cool": 2}' | http PUT http://localhost:5000/review

# example of full json object
# {
#     "business_id": "6Lx2UqDBh4nJNst1sUkG5g",
#     "cool": 0,
#     "date": "2014-01-19 04:15:28",
#     "funny": 0,
#     "review_id": "L0e2zyoiackZ5a8nq1OtSw",
#     "stars": 5.0,
#     "text": "I have been buying my make up at Rouge for 5 years now and finally had an event to go to that I needed my make up done!!...",
#     "useful": 0,
#     "user_id": "8wVz-Jr9IETJRTTVxvRkeg"
# }


# config
PAGE_SIZE = 2


app = Flask(__name__)


@app.route('/reviews/', defaults={'page': 1}, methods=['GET'])
@app.route('/reviews/<int:page>', methods=['GET'])
def get_reviews(page):
    """
    Get all reviews
    """
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


@app.route('/business/<string:business_id>/', defaults={'page': 1}, methods=['GET'])
@app.route('/business/<string:business_id>/<int:page>', methods=['GET'])
def get_business(business_id, page):
    """
    Get all reviews for a business
    """
    session = get_session()
    stmt = session.prepare(
        'SELECT * FROM reviews_by_business_id WHERE business_id = ?')
    reviews = session.execute(stmt, [business_id])
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


@app.route('/user/<string:user_id>/', defaults={'page': 1}, methods=['GET'])
@app.route('/user/<string:user_id>/<int:page>', methods=['GET'])
def get_user(user_id, page):
    """
    Get all reviews for a user
    """
    session = get_session()
    stmt = session.prepare(
        'SELECT * FROM reviews_by_user_id WHERE user_id = ?')
    reviews = session.execute(stmt, [user_id])
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


@app.route('/review', methods=['PUT'])
def create_review():
    """
    Create a new review
    """
    data = request.get_json()
    try:
        review_id, business_id, user_id, stars, text, date, useful, funny, cool = json_review_validation(
            data)
    except Exception as e:
        return jsonify({"error": e.args}), 400

    session = get_session()
    stmt = session.prepare("\
        INSERT INTO reviews_by_review_id (review_id, business_id, user_id, text, stars, date, useful, funny, cool)\
        VALUES (?,?,?,?,?,?,?,?,?)\
    ")
    session.execute(
        stmt, [review_id, business_id, user_id, text, stars, date, useful, funny, cool])

    return jsonify({'status': 'ok', 'review_id': review_id})


@app.route('/review/<string:review_id>', methods=['PATCH'])
def update_review(review_id):
    """
    Update a review
    """
    data = request.get_json()
    session = get_session()

    stmt = session.prepare(
        'SELECT * FROM reviews_by_review_id WHERE review_id = ?')
    current_review = session.execute(stmt, [review_id]).one()
    current_review['stars'] = data['stars'] if 'stars' in data else current_review['stars']
    current_review['text'] = data['text'] if 'text' in data else current_review['text']
    current_review['useful'] = data['useful'] if 'useful' in data else current_review['useful']
    current_review['funny'] = data['funny'] if 'funny' in data else current_review['funny']
    current_review['cool'] = data['cool'] if 'cool' in data else current_review['cool']
    del current_review['date']

    try:
        review_id_DO_NOT_USE_HERE, business_id_DO_NOT_USE_HERE, user_id_DO_NOT_USE_HERE, stars, text, date, useful, funny, cool = json_review_validation(
            current_review)
    except Exception as e:
        return jsonify({"error": e.args}), 400

    stmt = session.prepare("\
        UPDATE reviews_by_review_id SET text = ?, stars = ?, date = ?, useful = ?, funny = ?, cool = ? WHERE review_id = ?\
    ")
    session.execute(stmt, [text, stars, date, useful, funny, cool, review_id])

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
