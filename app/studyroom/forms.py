from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired
from flask_babel import _, lazy_gettext as _l


class addroomForm(FlaskForm):
    roomname = StringField(_l('roomname'), validators=[DataRequired()])
    submit = SubmitField(_l('add'))
