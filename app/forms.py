from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app import db
from app.models import User
import sqlalchemy as sa
from flask_login import current_user




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

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    bio = TextAreaField('Bio')
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        
        if username.data != self.original_username:
            query = sa.select(User).where(User.username == username.data)
            user = db.session.scalars(query).one_or_none()

            if user:
                raise ValidationError("Please use another username")
            

class GoalForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=40)])
    body = TextAreaField("Your goal")
    submit = SubmitField('Submit')