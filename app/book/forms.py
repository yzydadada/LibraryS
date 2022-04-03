from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import ValidationError, DataRequired
from flask_babel import _, lazy_gettext as _l


class addbookForm(FlaskForm):
    image = FileField(_l('bookimage'),validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif'])])
    bookname = StringField(_l('bookname'), validators=[DataRequired()])
    submit = SubmitField(_l('add'))

class BooksSearchForm(FlaskForm):
    post = TextAreaField(_l('Search something'), validators=[DataRequired()])
    submit = SubmitField(_l('Search'))