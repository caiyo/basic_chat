import flask
from datetime import timedelta

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=7)

from app.routes import routes

