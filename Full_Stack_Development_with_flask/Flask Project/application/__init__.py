from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_restplus import Api


api = Api()

app = Flask(__name__)

# Setting the database and configuration using Config class in config.py file
app.config.from_object(Config)


db = MongoEngine()
db.init_app(app)
api.init_app(app)
# importing routes
from application import routes
