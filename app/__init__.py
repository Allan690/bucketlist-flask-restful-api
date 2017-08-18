# app/__init__.py

from flask import Flask
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from config import app_config

authorization = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'token'
    }
}

app = Flask(__name__)
api = Api(app, version='1.0',
          authorizations=authorization,
          title='Bucketlist API',
          description='Bucketlist RESTful API using Flask with Endpoints.',)

app.config.from_object(app_config['staging'])

# initialize db by instantiating SQLAlchemy
db = SQLAlchemy(app)

from app.models import User, BucketlistItems, Bucketlist, Session
