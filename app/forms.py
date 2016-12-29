from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Optional
from datetime import datetime


class AddForm(FlaskForm):
    item = StringField('item', validators=[DataRequired()])
    category = StringField('category', validators=[DataRequired()])
    start = DateTimeLocalField('start',
                               format='%Y-%m-%dT%H:%M',
                               default=datetime.now,
                               validators=[Optional()])
