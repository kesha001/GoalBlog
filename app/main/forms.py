from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask import request

from flask_babel import lazy_gettext as l_

class GoalForm(FlaskForm):
    title = StringField(l_("Title"), validators=[DataRequired(), Length(max=60)])
    body = TextAreaField(l_("Your goal"))
    submit = SubmitField(l_('Submit'))


class SearchForm(FlaskForm):

    q = StringField(l_("Search"), validators=[DataRequired(), Length(max=600)])
    # submit = SubmitField(l_('Submit'))

    def __init__(self, *args, **kwargs):
        
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'meta' not in kwargs:
            kwargs['meta'] = {'csrf': False}
        super().__init__(*args, **kwargs)
        