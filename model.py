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
    firms = db.relationship('Firm', backref='role_name')

class Firm(db.Model, UserMixin):
    __tablename__ = 'firm'
    id = db.Column(db.Integer, primary_key=True)
    emailf = db.Column(db.String(50), nullable=False)
    namef = db.Column(db.String(50), nullable=False)
    passwordf = db.Column(db.String(200), nullable=False)
    nemployees = db.Column(db.Integer, nullable=False)
    piva = db.Column(db.Integer, nullable=False)
    sector = db.Column(db.String(50), nullable=False)
    fatturato = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def firm_variables(self):
        """
        :return: List of all user variables which are then used in account_details.html
        the Keys are what users see on the page, the list[0] is what it's called in this Class
        and the list[1] is grabbing the data from current_user
        """
        user_details = {
            'id': ['id', current_user.id],
            'emailf': ['emailf', current_user.emailf],
            'namef': ['namef', current_user.namef],
            'passwordf': ['passwordf', current_user.passwordf],
            'nemployees': ['nemployees', current_user.nemployees],
            'piva': ['piva', current_user.piva],
            'sector': ['sector', current_user.sector],
            'fatturato': ['fatturato', current_user.fatturato],
        }
        return user_details


class feeds(db.Model):
    __tablename__ = 'feeds'
    _id = db.Column("id" , db.Integer , primary_key=True)
    username = db.Column(db.String(100))
    feedback = db.Column(db.String(1000))

    def __init__(self , username , feedback):
        self.username = username
        self.feedback = feedback


class questions(db.Model):
    __tablename__ = 'question'
    _id = db.Column("id" , db.Integer , primary_key=True)
    username = db.Column(db.String(100))
    question = db.Column(db.String(1000))

    def __init__(self , username , question):
        self.username = username
        self.question = question


class answers(db.Model):
    __tablename__ = 'answer'
    id = db.Column("id" , db.Integer , primary_key=True)
    idQ = db.Column("idQ" , db.Integer)
    userAnswer = db.Column(db.String(100))
    answer = db.Column(db.String(1000))

    def __init__(self ,idQ ,  userAnswer, answer):
        self.idQ = idQ
        self.userAnswer = userAnswer
        self.answer = answer