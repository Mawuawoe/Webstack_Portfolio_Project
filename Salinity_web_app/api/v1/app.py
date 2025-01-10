#!/usr/bin/python3
""" Flask Application"""
import sys
sys.path.append("../../")
from models import storage
from flask import Flask, make_response, jsonify
from os import environ
from api.v1.views import app_views
from flask_jwt_extended import JWTManager
from flasgger import Swagger


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JWT_SECRET_KEY'] = 'my_jwt_secret_key'
jwt = JWTManager(app)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_founf(error):
    """
    404 Error

    responses:
    404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

app.config['SWAGGER'] = {
    'title': 'Webstack_portfolio_project- Salinity Web_app Restful API',
    'uiversion': 3
}

Swagger(app)


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
