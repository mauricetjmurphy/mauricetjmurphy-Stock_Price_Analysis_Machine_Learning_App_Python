import torch
from flask import Flask
from app.config import Config
from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config.from_object(Config)

mongodb_client = PyMongo(app)
db = mongodb_client.db
users = db.users


from app import routes
