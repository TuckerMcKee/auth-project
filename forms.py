from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length 

class RegisterUserForm(FlaskForm):
    """form for registering users"""

    username = StringField("Username")
    password = PasswordField("Password", validators=[DataRequired()])
    first_name = StringField("First name", validators=[DataRequired(),Length(max=30)])
    last_name = StringField("Last name", validators=[DataRequired(),Length(max=30)])
    email = StringField("Email", validators=[DataRequired(),Length(max=50)])

class LoginUserForm(FlaskForm):
    """form for logging in users"""

    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class FeedbackForm(FlaskForm):
    """form for adding feedback"""

    title = StringField("title",validators=[DataRequired(),Length(max=100)])
    content = StringField("content", validators=[DataRequired()])    
    


    