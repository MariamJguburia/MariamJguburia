from flask_wtf import FlaskForm
from wtforms.fields import (StringField, PasswordField, IntegerField,
                            DateField, RadioField, SelectField,
                            SubmitField)
from wtforms.validators import DataRequired, equal_to, length
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed


class RegisterForm(FlaskForm):
    username = StringField("Enter Username", validators=[
        DataRequired()
    ])
    password = PasswordField("Enter Password", validators=[
        DataRequired(),
        length(min=6, max=24),
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        equal_to("password", message="Passwords don't match :(.")
    ])
    role = SelectField("Register As", choices=[
        ("Guest", 'Guest'),
        ("Admin", 'Admin')
    ], validate_choice=False)

    register = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField()
    password = PasswordField()

    login = SubmitField("Log In")


class PlaceForm(FlaskForm):
    image = FileField("Upload place poster")
    title = StringField("Enter Place Title")
    known_since = IntegerField("Enter Place Known Since Year")
    description = StringField("Enter Place Description")
    flag = FileField("Upload Country Flag")
    submit = SubmitField("Add Place")

class ReviewForm(FlaskForm):
    text = StringField("Review", validators=[DataRequired()])
    submit = SubmitField("Submit")
