from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '67647b69afe78f4932724f9b94de2023ff8913961b057c5d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shadechase_primary.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flask_app import routes
