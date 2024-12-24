import sqlite3, random, os
from hashlib import sha256
from dotenv import load_dotenv

load_dotenv()

class UserMeet():

	def __init__(self, db_path = os.getenv('DB_NAME')):
		self.db_path = db_path

	def _connect(self):
		return sqlite3.connect(os.getenv('DB_NAME'))
	
	def check_if_user_is_signed(self, user_id: int, meet_id: int) -> bool:
		with self._connect() as conn:
			cursor = conn.cursor()

			cursor.execute("SELECT id FROM users_meets WHERE users_id = ? AND meets_id = ?", (user_id, meet_id,))

			found = cursor.fetchone()

			return found is not None
		
	def toggle_join_user(self, user_id: int, meet_id: int):
		with self._connect() as conn:
			cursor = conn.cursor()
			user_is_signed = self.check_if_user_is_signed(user_id, meet_id)


			if(user_is_signed):
				cursor.execute("DELETE FROM users_meets WHERE users_id = ? AND meets_id = ?", (user_id, meet_id,))
				conn.commit()
				return {
					'action': 'DELETE'
				}
			
			id = self._ensure_unique_id()

			cursor.execute('''
				INSERT INTO users_meets (id, users_id, meets_id)
				VALUES(?, ?, ?)
				''', (id, user_id, meet_id))
			
			conn.commit()
			
			return {
				'action': 'INSERT'
			}

	def _ensure_unique_id(self, int_from = 100000000, int_to = 999999999) -> int:
		with self._connect() as conn: 
			cursor = conn.cursor()
			id = random.randint(int_from, int_to)
			while True: 
				cursor.execute('SELECT * FROM users_meets WHERE id = ?', (id, ))
				res = cursor.fetchone()

				if(res is None):
					break
				else:
					id = random.randint(int_from, int_to)

			return id

	