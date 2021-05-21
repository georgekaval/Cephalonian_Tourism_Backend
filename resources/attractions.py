import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

from flask_login import current_user, login_required

attraction = Blueprint('attractions', 'attraction')

@attraction.route('/', methods=['GET'])
def attractions_index():
    try:
        # for each resource named attraction in the database, convert to a python dictionary
        attraction_dicts = [model_to_dict(attraction) for attraction in models.Attraction.select()]
        print(attraction_dicts)
        # Convert the following to JSON and send to the browser
        return jsonify(data=attraction_dicts, status={"code":200, "message": "Success"})
        # If you can not located this resource, send this error message
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@attraction.route('/', methods=["POST"])
def create_attractions():
    # receive request from browser and convert the JSON data sent to python dictionary data
    payload = request.get_json()
    # create the resource into the database throught the Attraction model using the data received from the request
    new_attraction = models.Attraction.create(name=payload['name'], location=payload['location'], image=payload['image'], info=payload['info'])
    # convert the newly created database data that is in model form to python dictionary
    attraction_dict = model_to_dict(new_attraction)
    # Convert the following to JSON and send to the browser
    return jsonify(data=attraction_dict, status={"code":201, "message": "Success"})

@attraction.route('/<id>', methods=["GET"])
def get_one_attraction(id):
    # find resource by its ID from the database
    attraction = models.Attraction.get_by_id(id)
    # Convert the following to JSON and send to the browser
    return jsonify(
    # changing the resource from the model format to a dictionary format
        data=model_to_dict(attraction),
        message="Successfully showed attraction",
        status=200
    ), 200

@attraction.route('/<id>', methods=["PUT"])
def update_attraction(id):
    # recieve request from browser and convert the JSON data to python dictionary
    payload = request.get_json()
    # update the database where the id sent from browser coincides with the database resource id and update with the data sent. Execute is just a built in method needed for update to work
    models.Attraction.update(**payload).where(models.Attraction.id==id).execute()
    # convert the following to JSON and send to the browser
    return jsonify(
        # change the resource from the model format to a dictionary format
        data=model_to_dict(models.Attraction.get_by_id(id)),
        status=200,
        message="Resource updated successfully"
    ),200

@attraction.route('/<id>', methods=["DELETE"])
def delete_attraction(id):
    models.Attraction.delete().where(models.Attraction.id==id).execute()
    return jsonify(
        status=200,
        message="Successfully deleted resource"
    ), 200
