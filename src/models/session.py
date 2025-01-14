import random, os, base64, sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class Session():
	def __init__(self, db_path = os.getenv('DB_NAME')):
		self.db_path = db_path
		self.file_path = './storage/data/session.dat'

	def _connect(self):
		return sqlite3.connect(os.getenv('DB_NAME'))

	def create_session(self, user_id):
		with self._connect() as conn:
			cursor = conn.cursor()

			id = self._ensure_unique_id()
			token = self._generate_session_token()
			current_date = datetime.now()
			valid_until = current_date + timedelta(days = 14)

			cursor.execute(''' 
				INSERT INTO
					sessions(id, token, valid_until, users_id)
				VALUES(?, ?, ?, ?)
			''', (id, token, valid_until, user_id))
			conn.commit()
			self._store_session(token)

	def delete_session(self, token):
		from utils.global_state import global_state
		with self._connect() as conn:
			cursor = conn.cursor()
			
			cursor.execute("UPDATE sessions SET is_active = 0 WHERE token = ?", (token, ))
			conn.commit()
			
			global_state.set_init()
			self.remove_session()

	def get_user_by_token(self, token):
		from models.user import User
		with self._connect() as conn:
			cursor = conn.cursor()

			cursor.execute('''
				SELECT users.email, sessions.users_id, sessions.valid_until 
				FROM sessions
				INNER JOIN users
				ON sessions.users_id = users.id
				WHERE 
					token = ? 
					AND is_active = 1 
					AND valid_until > CURRENT_TIMESTAMP
			''', (token, ))

			session = cursor.fetchone()	
			
			if session is None:
				print("Session is not valid...")
				return {
					'found': False
				}
			
			email = session[0]
			return User().get_user_by_email(email)
		
	def get_session_token_from_file(self):
		directory = os.path.dirname(self.file_path)

		if not os.path.exists(directory):
			os.makedirs(directory)

		if not os.path.exists(self.file_path):
			with open(self.file_path, 'w') as file:
				file.write('')
		
		with open(self.file_path, 'r') as file:
			return file.read()
	
	def remove_session(self):
		with open(self.file_path, 'w') as file:
			file.write('')

	def _store_session(self, token):
		with open(self.file_path, 'w') as file:
			file.write(token)

	def _ensure_unique_id(self, int_from = 1000000000, int_to = 9999999999) -> int:
		with self._connect() as conn: 
			cursor = conn.cursor()
			id = random.randint(int_from, int_to)
			while True: 
				cursor.execute('SELECT * FROM sessions WHERE id = ?', (id, ))
				res = cursor.fetchone()

				if res is None:
					break
				else:
					id = random.randint(int_from, int_to)

			return id
		
	
	def _generate_session_token(self):
		return base64.b64encode(os.urandom(32)).decode('utf-8')