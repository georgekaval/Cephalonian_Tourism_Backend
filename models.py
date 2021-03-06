import os
from peewee import *
import datetime
from flask_login import UserMixin
from playhouse.db_url import connect

# DATABASE = PostgresqlDatabase('attractions', user='postgres')
DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///attractions.sqlite')
# Connect to the database URL defined in the environment, falling
# back to a local Sqlite database if no database URL is specified.

class User(UserMixin, Model):
    username=CharField(unique=True, null=False, max_length=15)
    email=CharField(unique=True, null=False)
    password=CharField(null=False)
    admin=BooleanField(default=False)
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
    user=ForeignKeyField(User, backref="my_reviews")
    review=TextField(null=False)
    attraction=  ForeignKeyField(Attraction, backref="my_reviews")
    create_at: DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Attraction, Review], safe=True)
    print("Connected to the database and created tables if they werent already there")
    DATABASE.close()
