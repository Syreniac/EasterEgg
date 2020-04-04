from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return "Hello world"

@app.route('/create')
def cookie_create():
	return render_template('create.html', name="Create")
