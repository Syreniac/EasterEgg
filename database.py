from pydblite import Base
from flask_login import UserMixin

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
		
	def save(self):
		try:
			if self.id is None:
				self.id = db.insert(username=self.username, password=self.password, eggs=self.eggs)
			else:
				db.update(self.id, username=self.username, password=self.password, eggs=self.eggs)
			db.commit()
			return true
		except Exception as E:
			return false

def load_user(user_id):
	return User(**db[int(user_id)])

if db.exists:
	db.open()
	
user = User(username='Test', password='Hunter2', eggs=['cs-tc3-dev100'])
user.save()
user = load_user(user.get_id())
print(user.eggs)