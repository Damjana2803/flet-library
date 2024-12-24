import sqlite3, random, os
from hashlib import sha256
from dotenv import load_dotenv
from models.faculty import Faculty

load_dotenv()

class User: 
	def __init__(self, db_path = os.getenv('DB_NAME')):
		self.db_path = db_path

	def _connect(self):
		return sqlite3.connect(self.db_path)

	def create_user(self, name: str, email: str, password: str, faculty: str) -> bool:
		with self._connect() as conn:
			try:
				cursor = conn.cursor()
				hashed_password = self._hash_password(password)
				id = self._ensure_unique_id()				

				cursor.execute('''
					INSERT INTO 
						users(id, name, email, password, faculty_id) 
					VALUES(?, ?, ?, ?, ?)
				''', (id, name, email, hashed_password, faculty))

				conn.commit()
				return True
			except:
				return False

	def get_user_by_email(self, email: str):
		with self._connect() as conn:
			cursor = conn.cursor()
			cursor.execute('''
				SELECT users.id, users.name, users.email, users.is_admin, faculties.name
				FROM users
				LEFT JOIN faculties 
				ON faculties.id = users.faculty_id
				WHERE users.email = ?
			''', (email, ))

			user = cursor.fetchone()
			
			if(user is None):
				return {
					'found': False
				}

			return {
				'found': True,
				'id': user[0],
				'name': user[1],
				'email': user[2],
				'is_admin': user[3],
				'faculty': user[4]
			}

	def login_user(self, email, password):
		from models.session import Session
		with self._connect() as conn:
			cursor = conn.cursor()
			hashed_password = self._hash_password(password)
			cursor.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, hashed_password))

			res = cursor.fetchone()

			if(res is None):
				return {
					'logged': False
				}
			
			user = self.get_user_by_email(email)

			Session().create_session(user_id = user['id'])
			
			user['logged'] = True
			return user

	def _hash_password(self, password: str) -> str:
		return sha256(password.encode('utf-8')).hexdigest()
	
	def _ensure_unique_id(self, int_from = 100000000, int_to = 999999999) -> int:
		with self._connect() as conn: 
			cursor = conn.cursor()
			id = random.randint(int_from, int_to)
			while True: 
				cursor.execute('SELECT * FROM users WHERE id = ?', (id, ))
				res = cursor.fetchone()

				if(res is None):
					break
				else:
					id = random.randint(int_from, int_to)

			return id

	