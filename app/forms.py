from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    item = StringField('item', validators=[DataRequired()])
    category = StringField('category', validators=[DataRequired()])
