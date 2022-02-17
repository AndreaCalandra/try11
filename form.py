from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length, ValidationError
import email_validator
from model import User



class formRegisteration(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(min=3,max=25)])
    familyname = StringField('Family Name',validators=[DataRequired(),Length(min=3,max=25)])
    usern = StringField('Usern', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired(),Length(min=6,max=20)])
    isee = IntegerField('isee', validators=[DataRequired()])
    age = IntegerField('age', validators=[DataRequired()])
    profession = StringField('profession', validators=[DataRequired()])
    number_child = IntegerField('number_child', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user_check = User.query.filter_by(username=self.email.data).first()
        if user_check:
            raise ValidationError('This user has been register before or taken')


class loginForm(FlaskForm):
    username = StringField('Name',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[Length(min=3,max=15),DataRequired()])
    submit = SubmitField('Login')


class EditProfileForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(min=3,max=25)])
    familyname = StringField('Family Name',validators=[DataRequired(),Length(min=3,max=25)])
    usern = StringField('Usern', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired(),Length(min=6,max=20)])
    isee = IntegerField('isee', validators=[DataRequired()])
    age = IntegerField('age', validators=[DataRequired()])
    profession = StringField('profession', validators=[DataRequired()])
    number_child = IntegerField('number_child', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_name, original_familyname, original_usern, original_email,
                 original_password, original_isee, original_age, original_profession, original_number_child,
                 *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
        self.original_familyname = original_familyname
        self.original_usern = original_usern
        self.original_email = original_email
        self.original_password = original_password
        self.original_isee = original_isee
        self.original_age = original_age
        self.original_profession = original_profession
        self.original_number_child = original_number_child

    def validate_username(self, usern):
        if usern.data != self.original_usern:
            user = User.query.filter_by(username=self.usern.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user_check = User.query.filter_by(username=self.email.data).first()
            if user_check:
                raise ValidationError('This user has been register before or taken')


class firmformRegisteration(FlaskForm):
    emailf = StringField('Email', validators=[DataRequired(), Email()])
    namef = StringField('Name',validators=[DataRequired(),Length(min=3,max=25)])
    passwordf = PasswordField('Password',validators=[DataRequired(),Length(min=6,max=20)])
    nemployees = IntegerField('Number of employees', validators=[DataRequired()])
    piva = IntegerField('Partita iva', validators=[DataRequired()])
    sector = StringField('Sector',validators=[DataRequired(),Length(min=3,max=25)])
    fatturato = IntegerField('Fatturato', validators=[DataRequired()])
    submit = SubmitField('Register')


class firmloginForm(FlaskForm):
    piva = StringField('partita iva',validators=[DataRequired(),Email()])
    passwordf = PasswordField('Password',validators=[Length(min=3,max=15),DataRequired()])
    submit = SubmitField('Login')