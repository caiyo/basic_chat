import flask
from datetime import timedelta
from flask_socketio import SocketIO

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=7)

socketio = SocketIO(app)

from app.routes import routes
from app.routes import sockets

