import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

from flask_login import current_user, login_required

attraction = Blueprint('attractions', 'attraction')

@attraction.route('/', methods=['GET'])
def attractions_index():
    try:
        attraction_dicts = [model_to_dict(attraction) for attraction in models.Attraction.select()]
        print(attraction_dicts)
        return jsonify(data=attraction_dicts, status={"code":200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@attraction.route('/', methods=["POST"])
def create_attractions():
    payload = request.get_json()
    print(payload)

    new_attraction = models.Attraction.create(name=payload['name'], location=payload['location'], image=payload['image'], info=payload['info'])
    print(new_attraction)
    print(new_attraction.__dict__)
    print(dir(attraction))
    print(model_to_dict(new_attraction), 'model to dict')
    attraction_dict = model_to_dict(new_attraction)
    return jsonify(data=attraction_dict, status={"code":201, "message": "Success"})
