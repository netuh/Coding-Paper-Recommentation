from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, SelectMultipleField
from wtforms.validators import NumberRange


class SelectArticleForm(FlaskForm):

    # designs = SelectField(u'Designs', choices=[(
    #     'cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    designs = SelectField(u'Designs', choices=[])
    #tasks = SelectMultipleField(u'Task Type', choices=['COMPREHENSION', 'CONSTRUCTION', 'MAINTENANCE', 'TEST', 'DEGUGGING', 'INSPECTION', 'COMPREENSION', 'REVIEW'])
    tasks = SelectMultipleField(u'Task Type')
    measurements = SelectMultipleField(u'Measuriments')
    sample = SelectField(u'Sample Type', choices=[
                         ('Professional', 'Professional'), ('Student', 'Student'), ('All', 'All')])
    submit = SubmitField('Submit')
