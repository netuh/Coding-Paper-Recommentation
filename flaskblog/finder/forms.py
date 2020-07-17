from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, SelectMultipleField, BooleanField, IntegerField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.widgets import html5
from wtforms.validators import NumberRange


class SelectArticleForm(FlaskForm):
    max_value = 200
    min_value = 5
    sample_size_min = IntegerField(
        'Telephone', [NumberRange(min=min_value, max=max_value)], widget=html5.NumberInput(), default=min_value)
    sample_size_max = IntegerField(
        'Telephone', [NumberRange(min=min_value, max=max_value)], default=max_value)
    designs = SelectField('Design of Experiments')
    performed_tasks = SelectMultipleField('Task Types')
    recruting_type = SelectMultipleField('Recruitments')
    profile_type = SelectMultipleField('Profiles')
    nature_of_data = SelectMultipleField(
        'Nature of Data Source')
    duration = SelectField('Duration')
    lab_settings = BooleanField(
        'Performed in a Lab')
    list_all = SubmitField('List All')
