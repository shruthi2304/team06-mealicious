from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextField,DateTimeField,IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from app.models import UserProfile

class LoginForm(FlaskForm):
    email = TextField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    email = TextField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    dob = StringField('Date of Birth',validators=[DataRequired()])
    # weight = IntegerField('Weight', validators=[DataRequired()])
    # profession = TextField('Profession', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = UserProfile.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')