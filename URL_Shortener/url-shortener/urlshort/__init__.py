from . import urlshort
from flask import Flask


def create_app(test_config=None):


    app = Flask(__name__)
    # Secret key to send the data securely between different pages. It needs to be random and long
    app.secret_key = 'if4398fh494cm8m9h934fr934f34f'

    from . import urlshort
    app.register_blueprint(urlshort.app)

    return app
