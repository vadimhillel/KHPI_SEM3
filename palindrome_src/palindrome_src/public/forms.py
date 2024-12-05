from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp

class PalindromeForm(FlaskForm):
    number = StringField(
        "Enter a Positive Integer",
        validators=[
            DataRequired(message="This field cannot be empty."),
            Regexp(r"^\d+$", message="Only positive integers are allowed."),
        ],
    )
    submit = SubmitField("Check Palindrome")
