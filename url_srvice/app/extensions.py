from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_apispec import FlaskApiSpec

db = SQLAlchemy()
auth = HTTPBasicAuth()
docs = FlaskApiSpec()