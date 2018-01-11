from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('config.py')
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)

from project import routes
