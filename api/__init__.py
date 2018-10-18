from config import Config
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

import os
basedir = os.path.abspath(os.path.dirname(__file__) + '/..')

# Initialize app
app = Flask(__name__)
app.config.from_object(Config)
api = Api(app, prefix='/api')
auth = HTTPBasicAuth()

# Use separate (temporary) database for testing
if app.config['TESTING']:
    app.config['DATABASE'] = 'test_' + app.config['DATABASE']

# Initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, app.config['DATABASE'])
db = SQLAlchemy(app)
@app.before_first_request
def create_tables():
    db.create_all()

from . import views, models
