import torch
from flask import Flask
from app.config import Config
from flask_pymongo import PyMongo


app = Flask(__name__)
# model = torch.load('app/models/model.pth', map_location=torch.device('cpu'))
app.config.from_object(Config)

mongo = PyMongo(app)
db = mongo.db
users = db.users

from app import routes
