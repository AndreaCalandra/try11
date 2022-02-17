from app import db
from flask_login import UserMixin, current_user


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    usern = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    isee = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    number_child = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return "<User %r>" % self.name

    def user_variables(self):
        """
        :return: List of all user variables which are then used in account_details.html
        the Keys are what users see on the page, the list[0] is what it's called in this Class
        and the list[1] is grabbing the data from current_user
        """
        user_details = {
            'id': ['id', current_user.id],
            'username': ['username', current_user.username],
            'usern': ['usern', current_user.usern],
            'name': ['name', current_user.name],
            'password': ['password', current_user.password],
            'isee': ['isee', current_user.isee],
            'age': ['age', current_user.age],
            'profession': ['profession', current_user.profession],
            'number_child': ['number_child', current_user.number_child]
        }
        return user_details

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', backref='role_name')

class Firm(db.Model, UserMixin):
    __tablename__ = 'firm'
    idf = db.Column(db.Integer, primary_key=True)
    emailf = db.Column(db.String(50), nullable=False)
    namef = db.Column(db.String(50), nullable=False)
    passwordf = db.Column(db.String(200), nullable=False)
    nemployees = db.Column(db.Integer, nullable=False)
    piva = db.Column(db.Integer, nullable=False)
    sector = db.Column(db.String(50), nullable=False)
    fatturato = db.Column(db.Integer, nullable=False)