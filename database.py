from pydblite import Base
from flask_login import UserMixin
import traceback 

db = Base('users')

# Password stored as a hash
db.create('username','eggs','email', mode='open')

class User(UserMixin):
	def __init__(self, **kwargs):
		self.id =  kwargs['__id__'] if '__id__' in kwargs else None
		self.username = kwargs['username']
		self.eggs = kwargs['eggs'] if 'eggs' in kwargs else set()

	def check_password(self, password):
		return True
		
	def save(self):
		try:
			if self.id is None:
				self.id = db.insert(username=self.username, eggs=self.eggs)
			else:
				db.update(db[self.id], username=self.username, eggs=self.eggs)
			db.commit()
			return True
		except Exception as E:
			traceback.print_exc(E)
			return False
			
def create_user(username, email):
	return User(username = username, email = email)

def load_user(user_id):
	return User(**db[int(user_id)])
	
def find_user_by_username(username):
	for user in db:
		if user['username'] == username:
			return User(**user)
	return None

def username_exists(username):
	for user in db:
		print(user['username'])
		if user['username'] == username:
			return True
	return False

def email_exists(email):
	for user in db:
		if user['email'] == email:
			return True
	return False
	
def get_all_users():
	l = []
	for user in db:
		l.append(user)
	return l

if db.exists:
	db.open()