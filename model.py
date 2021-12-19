from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),unique=True,nullable=False)
    usern = db.Column(db.String(50),nullable=False)
    name = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return "<User %r>" % self.name

