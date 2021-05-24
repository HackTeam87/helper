#! /usr/bin/python3
from flask import Flask
from config import Configuration
from flask_sslify import SSLify
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Configuration)
sslify = SSLify(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
from models import *

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
