from flask import Flask, jsonify, g

from flask_cors import CORS

from flask_login import LoginManager

from dotenv import load_dotenv

from resources.attractions import attraction
from resources.reviews import review
# from resources.users import users

import models

import os

load_dotenv()

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_APP_SECRET")

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return models.User.get(models.User.id == user_id)

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

CORS(attraction, origins=['http://localhost:3000'], supports_credentials=True)
# CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
CORS(review, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(attraction, url_prefix='/api/v1/attractions')
# app.register_blueprint(user, url_prefix='/api/v1/users')
app.register_blueprint(review, url_prefix='/api/v1/reviews')

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
