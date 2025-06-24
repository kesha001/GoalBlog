from app import db
from app.models import User
import sqlalchemy as sa

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), 
                                                            EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Submit')

    def validate_username(form, username):

        query = sa.select(User).where(User.username == username.data)
        user = db.session.scalars(query).one_or_none()

        if user:
            raise ValidationError("Please use another username")

    def validate_email(form, email):

        query = sa.select(User).where(User.email == email.data)
        user = db.session.scalars(query).one_or_none()

        if user:
            raise ValidationError("Please use another email")
        

class RequestResetPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), 
                                                            EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Submit')
