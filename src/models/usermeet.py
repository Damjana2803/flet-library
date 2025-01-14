import sqlite3, random, os
from hashlib import sha256
from dotenv import load_dotenv
from utils.helper_func import convert_sqlite3rows_to_dict

load_dotenv()

class UserMeet():

	def __init__(self, db_path = os.getenv('DB_NAME')):
		self.db_path = db_path

	def _connect(self):
		return sqlite3.connect(os.getenv('DB_NAME'))
	
	def get_all_joined_meets(self, user_id: int):
		with self._connect() as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()
		
			cursor.execute('''
				SELECT 
					users.id as users_id,
					users.name as users_name,
					faculties.name as faculty,
					meets.id as meets_id,
					meets.title as meets_title,
					meets.description as meets_description,
					meets.field as meets_field,
					meets.location as meets_location, 
					meets.start_date as meets_start_date,
					meets.start_time as meets_start_time,
					meets.users_limit as meets_user_limit,
					meets.created_by as meets_created_by,
					users_meets.comment AS users_meets_comment,
					users_meets.comment_time AS users_meets_comment_time,
					users_meets.stars AS users_meets_stars
				FROM users_meets
				INNER JOIN meets
				ON users_meets.meets_id = meets.id
				INNER JOIN users
				ON users_meets.users_id = users.id
				INNER JOIN faculties
				ON users.faculty_id = faculties.id
				WHERE users_meets.users_id = ?
			''', (user_id, ))

			meets = cursor.fetchall()

			converted_meets = convert_sqlite3rows_to_dict(meets)

			return converted_meets

	def check_if_user_is_signed(self, user_id: int, meet_id: int) -> bool:
		with self._connect() as conn:
			cursor = conn.cursor()

			cursor.execute("SELECT id FROM users_meets WHERE users_id = ? AND meets_id = ?", (user_id, meet_id,))

			found = cursor.fetchone()

			return found is not None
		
	def get_users_in_meet(self, meet_id: int):
		with self._connect() as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()
			
			cursor.execute('''
				SELECT 
					users.name AS users_name,
					users.email AS users_email,
					users_meets.stars AS rating,
					users_meets.comment AS comment
				FROM users
				INNER JOIN users_meets
				ON users_meets.users_id = users.id
				WHERE users_meets.meets_id = ?
			''', (meet_id, ))

			users = cursor.fetchall()

			converted_users = convert_sqlite3rows_to_dict(users)

			return converted_users
		
	def toggle_join_user(self, user_id: int, meet_id: int):
		with self._connect() as conn:
			cursor = conn.cursor()
			user_is_signed = self.check_if_user_is_signed(user_id, meet_id)


			if user_is_signed:
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

	def add_comment(self, user_id: int, meet_id: int, rating: int, comment: str):
		with self._connect() as conn:
			cursor = conn.cursor()

			if not self.check_if_user_is_signed(user_id, meet_id):
				return False
			
			cursor.execute('''
				UPDATE users_meets 
				SET 
					comment = ?,
					stars = ?
				WHERE meets_id = ?
				AND users_id = ?
			''', (comment, rating, meet_id, user_id))

			conn.commit()

			return True

	def _ensure_unique_id(self, int_from = 100000000, int_to = 999999999) -> int:
		with self._connect() as conn: 
			cursor = conn.cursor()
			id = random.randint(int_from, int_to)
			while True: 
				cursor.execute('SELECT * FROM users_meets WHERE id = ?', (id, ))
				res = cursor.fetchone()

				if res is None:
					break
				else:
					id = random.randint(int_from, int_to)

			return id

	