from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from database import username_exists, email_exists

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Register')

	def validate_username(self, username):
		if username_exists(username.data):
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		if email_exists(email.data):
			raise ValidationError('Please use a different email address.')