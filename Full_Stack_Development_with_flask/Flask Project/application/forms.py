from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , SubmitField, BooleanField

from wtforms.validators import DataRequired


# Creating forms using flask WT Forms.
class LoginForm(FlaskForm):
    #  StringField("Email" here Email is the label for input type  email
    email = StringField("Email",validators=[DataRequired()])
    password = StringField("Password",validators=[DataRequired()])
    remember_me = BooleanField("Remember Me") # Creating checkbox
    # We must use function call i.e. form.submit() to submit our data
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    email = StringField("Email",vaildators=[DataRequired()])
    password = StringField("Password",vaildators=[DataRequired()])
    password_confirm = StringField("Confirm Password",vaildators=[DataRequired()])
    first_name = StringField("First Name",vaildators=[DataRequired()])
    last_name = StringField("Last Name",vaildators=[DataRequired()])
    submit = SubmitField("Register Now")
