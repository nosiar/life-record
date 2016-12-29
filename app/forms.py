from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Optional
from datetime import datetime


class AddForm(FlaskForm):
    item = StringField('Item', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    start = DateTimeLocalField('Start',
                               format='%Y-%m-%dT%H:%M',
                               default=datetime.now,
                               validators=[Optional()])
