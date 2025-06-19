from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from app import db
from app.models import User
import sqlalchemy as sa

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
            

class FollowForm(FlaskForm):
    submit = SubmitField()