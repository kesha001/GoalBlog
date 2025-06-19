from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class GoalForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=40)])
    body = TextAreaField("Your goal")
    submit = SubmitField('Submit')