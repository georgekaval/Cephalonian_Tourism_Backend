from peewee import *
import datetime
from flask_login import UserMixin
DATABASE = SqliteDatabase('attractions.sqlite')

class User(UserMixin, Model):
    username=CharField(unique=True, null=False, max_length=15)
    email=CharField(unique=True, null=False)
    password=CharField(null=False)
    class Meta:
        database = DATABASE

class Attraction(Model):
    name = CharField(null=False)
    location = CharField(null=False)
    image = CharField(null=False)
    info = TextField(null=False)
    class Meta:
        database = DATABASE

class Review(Model):
    user=ForeignKeyField(User, backref="user_review")
    review=TextField(null=False)
    attraction=ForeignKeyField(Attraction, backref="attraction_review")
    create_at: DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Attraction, Review], safe=True)
    print("Connected to the database and created tables if they werent already there")
    DATABASE.close()
