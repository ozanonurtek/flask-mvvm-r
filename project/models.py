from project import app
from werkzeug.security import generate_password_hash, \
     check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(1000))
    isAdmin = db.Column(db.Boolean, default=False)
    event = db.relationship('Event', backref="user", cascade="all, delete-orphan", lazy='dynamic')

    def __init__(self,username, email, password, admin):
        self.username = username
        self.email = email
        self.set_password(password)
        self.isAdmin = admin

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
            return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Event(db.Model):
    __tablename__ = "Event"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), unique=True)
    # ForeignKey for one to many relationship
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def __init__(self, date):
        self.date = date
