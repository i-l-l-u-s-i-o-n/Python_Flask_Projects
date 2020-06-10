from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , SubmitField, BooleanField

from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User




# Creating forms using flask WT Forms.
class LoginForm(FlaskForm):
    #  StringField("Email" here Email is the label for input type  email
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=6,max=15)])
    remember_me = BooleanField("Remember Me") # Creating checkbox
    # We must use function call i.e. form.submit() to submit our data
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=6,max=15)])
    password_confirm = PasswordField("Confirm Password",validators=[DataRequired(),Length(min=6,max=15),EqualTo('password')])
    first_name = StringField("First Name",validators=[DataRequired(),Length(min=2,max=55)])
    last_name = StringField("Last Name",validators=[DataRequired(),Length(min=2,max=55)])
    submit = SubmitField("Register Now")

    # We must put field name i.e. email after 'validate_' to set the function name it will automatically validate that field
    def validate_email(self,email):

        # fetching record from database
        user = User.objects(email=email.data).first()
        if user:
            # Following will raise the error in the  view in which this email field is used i.e the register.html page
            raise ValidationError("Email is already in use. Pick another one.")


