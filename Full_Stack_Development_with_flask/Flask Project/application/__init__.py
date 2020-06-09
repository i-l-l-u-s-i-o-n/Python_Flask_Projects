from flask import Flask

app = Flask(__name__)

# importing routes
from application import routes
