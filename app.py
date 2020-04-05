from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import current_user, login_user, LoginManager, login_required, current_user
from database import load_user, find_user_by_username, create_user
from registration_form import RegistrationForm
from config import Config
from werkzeug.urls import url_parse

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign In')

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.user_loader(load_user)
login.login_view = 'register'

@app.route('/scoreboard')
def scoreboard():
	return "Hello world!"

@app.route('/easterEgg/<easter_egg>')
@login_required
def easter_egg(easter_egg ):
	print(current_user)
	return "You found "+easter_egg

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = find_user_by_username(form.username.data)
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=True)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)
	
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = create_user(form.username.data, form.email.data, form.password.data)
		user.save()
		flash('Congratulations, you are now a registered user!')
		login_user(user, remember=True)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('register.html', title='Register', form=form)