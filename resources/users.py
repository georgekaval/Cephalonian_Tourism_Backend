import models

from flask import request, Blueprint, jsonify

from flask_bcrypt import generate_password_hash, check_password_hash

from flask_login import login_user, current_user, logout_user

from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user')

# @user.route('/', methods=['GET'])
# def view_users():
#
@user.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(
            data={},
            status={"code": 401, "message": "A user with that name already exists"}
            )
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        created_user = models.User.create(**payload)
        login_user(created_user)
        created_user_dict = model_to_dict(created_user)
        print(created_user_dict)
        del created_user_dict['password']
        return jsonify(
            data=created_user_dict,
            status={"code": 201, "message": "Success"}
            )

@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    print('payload', payload)
    try:
        user = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            print(user, 'this is the user')
            return jsonify(
                data=user_dict,
                status={
                    "code":200,
                    "message": "Success"
                }
            )
        else:
            return jsonify(
                data={},
                status={
                    "code": 401,
                    "message": "Password is incorrect"
                }
            )
    except models.DoesNotExist:
        return jsonify(
            data={},
            status={
                "code": 401,
                "message": "Username is incorrect"
            }
        )

@user.route('/logout', methods=["GET"])
def logout():
    logout_user()
    return jsonify(
        data={},
        status=200,
        message='successful logout'
    ), 200
