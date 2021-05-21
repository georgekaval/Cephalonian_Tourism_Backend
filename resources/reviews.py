import models

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict

from flask_login import current_user, login_required

review = Blueprint('reviews', 'review')

@review.route('/', methods=["GET"])
def review_index():
    try:
        review_dicts = [model_to_dict(review) for review in models.Review.select()]
        return jsonify({
            'data': review_dicts,
            'message': "Successfully found reviews",
            'status': 200
        }),200
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@review.route('/', methods=['POST'])
def create_review():
    payload = request.get_json()
    new_review = models.Review.create(**payload)
    review_dict = model_to_dict(new_review)
    return jsonify(
        data=review_dict,
        message="Successfully created review",
        status=201
    ), 201

@review.route('/<id>', methods=["GET"])
def get_one_review(id):
    review = models.Review.get_by_id(id)
    return jsonify(
        data=model_to_dict(review),
        message="Successfully showed review",
        status=200
    ), 200

@review.route('/<id>', methods=["PUT"])
def update_review(id):
    payload = request.get_json()
    models.Review.update(**payload).where(models.Review.id==id).execute()
    return jsonify(
        data=model_to_dict(models.Review.get_by_id(id)),
        message="Successfully updated review",
        status=200
    ), 200

@review.route('/<id>', methods=["DELETE"])
def delete_review(id):
    models.Review.delete().where(models.Review.id==id).execute()
    return jsonify(
        status=200,
        message="Successfully deleted resource"
    ), 200
