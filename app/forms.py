from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import InputRequired, Optional
from datetime import datetime


class AddForm(FlaskForm):
    item = StringField('Item', validators=[InputRequired()])
    category = StringField('Category', validators=[InputRequired()])
    start = DateTimeLocalField('Start',
                               format='%Y-%m-%dT%H:%M',
                               default=datetime.now,
                               validators=[Optional()])


class ActForm(FlaskForm):
    category = RadioField('label',
                          choices=[('piano', '피아노'), ('workout', '운동')],
                          default='piano',
                          validators=[InputRequired()])
