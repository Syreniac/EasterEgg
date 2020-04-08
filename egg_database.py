from pydblite import Base
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
import sys

db = Base('eggs')

db.create('name', 'key', 'seed', mode='open')

def validate_egg_key(name, key):
	for egg in db:
		if egg['name'] == name:
			return check_password_hash(egg['key'], key)
	return False
	
def egg_exists(name):
	for egg in db:
		if egg['name'] == name:
			return True
	return False
	
def get_egg_seed(name):
	for egg in db:
		if egg['name'] == name:
			return egg['seed']
	return 0
	
def create_egg(name):
	unhashed_key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
	key = generate_password_hash(unhashed_key)
	seed = random.randint(1, 2**32)
	db.insert(name=name, key=key, seed=seed)
	db.commit()
	return {'name':name, 'key':unhashed_key, 'seed':seed}
	
	
if db.exists:
	db.open()