from pydblite import Base

db = Base('easteregg')

db.create('username','password','eggs', mode='open')

if db.exists:
	db.open()
	
db.insert(username='testuser', password='hunter2', eggs=['cs-tc3-dev100'])