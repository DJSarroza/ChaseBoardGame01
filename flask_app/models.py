from datetime import datetime
from flask_app import db, login_manager
from flask_login import UserMixin

# ==============================================================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==============================================================
# User Accounts and Posts

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    image_file = db.Column(db.String(128), nullable=False, default='default.jpg')
    password = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(16), nullable=False, default='BASIC')
    joined_game_session = db.Column(db.String(8))

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

# ==============================================================
# Game Session


class GameSessions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_code = db.Column(db.String(8))
    host_username = db.Column(db.String(16))     # Foreign key of User table (username)
    status = db.Column(db.String(16), default="CREATED")
    data1 = db.Column(db.String(128))
    data2 = db.Column(db.String(128))
    data3 = db.Column(db.String(128))

    last_activity = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)     # Touched after every GameEvent
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


# ==============================================================
# Game Mechanics

class Terrain(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    layer1_img = db.Column(db.String(128))
    layer2_img = db.Column(db.String(128))
    layer3_img = db.Column(db.String(128))
    desirable_to = db.Column(db.String(128))
    undesirable_to = db.Column(db.String(128))


class Races(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16))
    description1 = db.Column(db.String(128))
    description2 = db.Column(db.String(128))
    description3 = db.Column(db.String(128))

    sprite_pack = db.Column(db.String(128))

    starting_dp = db.Column(db.Integer, default=0)
    starting_hp = db.Column(db.Integer, default=0)
    starting_mp = db.Column(db.Integer, default=0)
    starting_ap = db.Column(db.Integer, default=0)

    default_max_dp = db.Column(db.Integer, default=5)
    default_max_hp = db.Column(db.Integer, default=5)
    default_max_mp = db.Column(db.Integer, default=8)
    default_max_ap = db.Column(db.Integer, default=3)

    data1 = db.Column(db.String(128))
    data2 = db.Column(db.String(128))
    data3 = db.Column(db.String(128))
    data4 = db.Column(db.String(128))
    data5 = db.Column(db.String(128))


class Actions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16))

    data1 = db.Column(db.String(128))
    data2 = db.Column(db.String(128))
    data3 = db.Column(db.String(128))

# ==============================================================
