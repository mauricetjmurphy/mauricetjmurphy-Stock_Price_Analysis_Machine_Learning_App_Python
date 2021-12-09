import torch
from flask import Flask
from app.config import Config
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)
db = mongo.db
users = db.users

from app import routes
