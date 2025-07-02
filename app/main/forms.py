from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

from flask_babel import lazy_gettext as l_

class GoalForm(FlaskForm):
    title = StringField(l_("Title"), validators=[DataRequired(), Length(max=60)])
    body = TextAreaField(l_("Your goal"))
    submit = SubmitField(l_('Submit'))
