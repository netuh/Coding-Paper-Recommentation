from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField
from wtforms.validators import NumberRange


class SelectArticleForm(FlaskForm):

    designs = SelectMultipleField(u'Programming Language', choices=[(
        'cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    tasks = SelectMultipleField(u'Programming Language', choices=[(
        'cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    measuriments = SelectMultipleField(u'Programming Language', choices=[(
        'cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    list_all = SubmitField('List All')
