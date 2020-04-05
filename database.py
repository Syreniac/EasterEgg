from pydblite import Base
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = Base('easteregg')

# Password stored as a hash
db.create('username','password','eggs', mode='open')

class User(UserMixin):
	def __init__(self, **kwargs):
		self.id =  kwargs['__id__'] if '__id__' in kwargs else None
		self.username = kwargs['username']
		# Stored as a hash 
		self.password = kwargs['password']
		self.eggs = kwargs['eggs']

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)
		
	def save(self):
		try:
			if self.id is None:
				self.id = db.insert(username=self.username, password=self.password, eggs=self.eggs)
			else:
				db.update(self.id, username=self.username, password=self.password, eggs=self.eggs)
			db.commit()
			return True
		except Exception as E:
			return False

def load_user(user_id):
	return User(**db[int(user_id)])
	
def find_user_by_username(username):
	for user in db:
		if user['username'] == username:
			return User(**user)
	return None

if db.exists:
	db.open()
	
user = User(username='Test', password=generate_password_hash('Hunter2'), eggs=['cs-tc3-dev100'])
user.save()
user = load_user(user.get_id())
print(user.eggs)