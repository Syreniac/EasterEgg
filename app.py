import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import current_user, login_user, LoginManager, login_required, current_user
from database import load_user, find_user_by_username, create_user, get_all_users
from registration_form import RegistrationForm
from config import Config
from werkzeug.urls import url_parse
from pubsub import pub
from flask_socketio import SocketIO, emit
from egg_database import validate_egg_key, egg_exists, create_egg, get_egg_seed
from flask import jsonify
from json import dumps


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign In')

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.user_loader(load_user)
login.login_view = 'register'
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

def listener(arg1,seed):
    print('Function listener1 received:')
    print('  arg1 =', arg1)
    socketio.emit('newmessage',{'message':arg1,'seed':seed})


pub.subscribe(listener, 'rootTopic')

@app.route('/')
@app.route('/scoreboard')
def scoreboard():
	return render_template('scoreboard.html', title='Scoreboard', all_users = sorted(get_all_users(), key = lambda x:  len(x['eggs']), reverse=True))

@app.route('/egg/<easter_egg>')
@login_required
def easter_egg(easter_egg ):
	key = request.args.get('key')
	if not validate_egg_key(easter_egg, key):
		return render_template('stop_cheating.html', title="Stop cheating!")
	if easter_egg in current_user.eggs:
		return render_template("duplicateEgg.html", title="You've already found this egg!")
	current_user.eggs.add(str(easter_egg))
	current_user.save()
	seed = get_egg_seed(easter_egg)
	pub.sendMessage('rootTopic', arg1=current_user.username+" found egg "+easter_egg, seed=seed)
	return render_template('foundEgg.html', title='You found an egg!', egg_name=easter_egg, egg_seed=seed)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('scoreboard'))
	form = LoginForm()
	if form.validate_on_submit():
		user = find_user_by_username(form.username.data)
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=True)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('scoreboard')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)
	
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('scoreboard'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = create_user(form.username.data, form.email.data, form.password.data)
		user.save()
		flash('Congratulations, you are now a registered user!')
		login_user(user, remember=True)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('scoreboard')
		return redirect(next_page)
	return render_template('register.html', title='Register', form=form)
	
@app.route('/add_egg/<location>', methods=['PUT'])
def add_egg(location):
	if egg_exists(location):
		return (dumps({'Error':"Egg already registered for that location"}),409)
	json = jsonify(create_egg(location))
	json.status_code = 200
	return json
	
	
@socketio.on('connect')
def connect():
    print('Client connected')

if __name__ == '__main__':
	try:
		socketio.run(app)
	except Exception as E:
		print(E)