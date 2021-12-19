from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError
import email_validator
from model import User



class formRegisteration(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(min=3,max=25)])
    familyname = StringField('Family Name',validators=[DataRequired(),Length(min=3,max=25)])
    usern = StringField('Usern', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired(),Length(min=6,max=20)])
    submit = SubmitField('Register')
