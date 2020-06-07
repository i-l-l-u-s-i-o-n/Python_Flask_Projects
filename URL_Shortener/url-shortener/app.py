from flask import Flask

app =Flask(__name__)


@app.route('/')
def home():
    return 'Hello Shivam!'


@app.route('/about')
def about():
    return "Shivam Shukla!"