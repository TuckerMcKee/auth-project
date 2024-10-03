from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True,nullable=False,unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    feedback = db.relationship('Feedback', backref='user')

    @classmethod
    def register(cls,username,pwd,first_name,last_name,email):
        """stores new user with hashed password and return user"""
        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username,password=hashed_utf8,first_name=first_name,last_name=last_name,email=email)
    
    @classmethod
    def authenticate(cls,username,pwd):
        """validate user and return user if valid else false"""
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False

class Feedback(db.Model):

    __tablename__ = 'feedback'   

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username', ondelete='CASCADE'), nullable=False)
