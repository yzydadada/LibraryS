from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired
from flask_babel import _, lazy_gettext as _l


class addbookForm(FlaskForm):
    bookname = StringField(_l('bookname'), validators=[DataRequired()])
    submit = SubmitField(_l('add'))
