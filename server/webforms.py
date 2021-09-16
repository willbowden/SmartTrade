from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class TestForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField('Go!')