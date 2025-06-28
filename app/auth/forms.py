from app import db
from app.models import User
import sqlalchemy as sa

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from flask_babel import lazy_gettext as l_

class LoginForm(FlaskForm):
    username = StringField(l_('Username'), validators=[DataRequired()])
    password = PasswordField(l_('Password'), validators=[DataRequired()])
    remember_me = BooleanField(l_('Remember Me'))
    submit = SubmitField(l_('Submit'))

class RegisterForm(FlaskForm):
    username = StringField(l_('Username'), validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(l_('Password'), validators=[DataRequired(), EqualTo('confirm')])
    confirm = PasswordField(l_('Confirm Password'), validators=[DataRequired(), 
                                                            EqualTo('password', message=l_('Passwords must match'))])
    submit = SubmitField(l_('Submit'))

    def validate_username(form, username):

        query = sa.select(User).where(User.username == username.data)
        user = db.session.scalars(query).one_or_none()

        if user:
            raise ValidationError(l_("Please use another username"))

    def validate_email(form, email):

        query = sa.select(User).where(User.email == email.data)
        user = db.session.scalars(query).one_or_none()

        if user:
            raise ValidationError(l_("Please use another email"))
        

class RequestResetPasswordForm(FlaskForm):
    email = EmailField(l_('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(l_('Submit'))

class ResetPasswordForm(FlaskForm):
    password = PasswordField(l_('New Password'), validators=[DataRequired(), EqualTo('confirm')])
    confirm = PasswordField(l_('Confirm Password'), validators=[DataRequired(), 
                                                            EqualTo('password', message=l_('Passwords must match'))])
    submit = SubmitField(l_('Submit'))
