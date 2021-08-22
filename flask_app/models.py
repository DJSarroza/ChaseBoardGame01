from datetime import datetime
from flask_app import db, login_manager
from flask_login import UserMixin

#==============================================================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#==============================================================

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    image_file = db.Column(db.String(128), nullable=False, default='default.jpg')
    password = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(16), nullable=False, default='BASIC')

    def __repr__(self):
        return f"User('{self.username}', {self.email}, {self.image_file})"


class UserRoles(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(16), nullable=False)
    attribute1 = db.Column(db.String(16), nullable=False)
    attribute2 = db.Column(db.String(16), nullable=False)
    attribute3 = db.Column(db.String(16), nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', {self.date_posted})"

