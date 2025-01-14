import random, os, sqlite3
from hashlib import sha256
from dotenv import load_dotenv
from models.faculty import Faculty
from utils.helper_func import convert_sqlite3rows_to_dict
load_dotenv()

class Meet:
	def __init__(self, db_path = os.getenv('DB_NAME')):
		self.db_path = db_path

	def _connect(self):
		return sqlite3.connect(self.db_path)

	def create_meet(self, title: str, description: str, field: str, location: str, start_date, start_time, users_limit: int, user_id: int) -> int:
		with self._connect() as conn:
			try:
				cursor = conn.cursor()
				id = self._ensure_unique_id()

				cursor.execute('''
					INSERT INTO 
						meets(id, title, description, field, location, start_date, start_time, users_limit, created_by)
					VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
				''', (id, title, description, field, location, start_date, start_time, users_limit, user_id))
				
				conn.commit()
				return {
					'success': True,
					'id': id
				}
			except Exception as e:
				print(e)
				return {
					'success': False
				}

	def get_meet_by_id(self, id: int):
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
					meets.created_by as meets_created_by
				FROM meets
				INNER JOIN users
				ON users.id = meets.created_by
				LEFT JOIN faculties
				ON users.faculty_id = faculties.id
				WHERE meets.id = ?
			''', (id, ))
			
			meet = cursor.fetchone()
			
			cursor.execute("SELECT COUNT(users_id) FROM users_meets WHERE meets_id = ?", (id, ))
		
			user_count = cursor.fetchone()

			if meet is None:
				return {
					'found': False
				}
			
			converted_meet = convert_sqlite3rows_to_dict(meet)
			converted_meet['found'] = True
			converted_meet['user_count'] = user_count[0]
			
			return converted_meet

	def get_all_valid_meets(self, user_id: int):
		with self._connect() as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()

			cursor.execute('''
				SELECT
					users.id AS users_id,
					users.name AS users_name,
					faculties.name AS faculty,
					meets.id AS meets_id,
					meets.title AS meets_title,
					meets.description AS meets_description,
					meets.field AS meets_field,
					meets.location AS meets_location, 
					meets.start_date AS meets_start_date,
					meets.start_time AS meets_start_time,
					meets.users_limit AS meets_users_limit,
					meets.created_by AS meets_created_by,
					COUNT(users_meets.users_id) AS user_count
				FROM meets
				INNER JOIN users
				ON users.id = meets.created_by
				LEFT JOIN faculties
				ON users.faculty_id = faculties.id
				LEFT JOIN users_meets 
				ON users_meets.meets_id = meets.id
				WHERE CURRENT_TIMESTAMP < DATETIME(DATE(start_date) || ' ' || TIME(start_time))
				AND meets.created_by != ?
				
				GROUP BY 
					meets.id,
					users.id,
					faculties.name,
					meets.title,
					meets.description,
					meets.field,
					meets.location,
					meets.start_date,
					meets.start_time,
					meets.users_limit,
					meets.created_by
				HAVING user_count < meets_users_limit
			''', (user_id, ))

			meets = cursor.fetchall()
			
			meets_dict = convert_sqlite3rows_to_dict(meets)
			return meets_dict

	def get_all_meets(self):
		with self._connect() as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()
			
			cursor.execute('''
				SELECT
					meets.id AS meets_id,
					meets.title AS meets_title,
					meets.field AS meets_field,
					meets.description AS meets_description,
					meets.start_date AS meets_start_date,
					meets.start_time AS meets_start_time,
					meets.location AS meets_location,
					meets.users_limit AS meets_users_limit,
					users.id AS users_id,
					users.name AS users_name,
					COUNT(users_meets.users_id) AS user_count
				FROM meets
				LEFT JOIN users_meets
				ON users_meets.meets_id = meets.id
				LEFT JOIN users
				ON meets.created_by = users.id
				GROUP BY meets.id, users.id
				ORDER BY DATETIME(DATE(meets.start_date) || ' ' || TIME(meets.start_time)) DESC
			''')

			meets = cursor.fetchall()
			meets_dict = convert_sqlite3rows_to_dict(meets)
			return meets_dict

	def edit_meet(self, id: int, title: str, desc: str):
		with self._connect() as conn:
			cursor = conn.cursor()

			cursor.execute('''
				UPDATE meets
				SET title = ?, description = ?
				WHERE id = ?
			''', (title, desc, id))

			conn.commit()

			return True
		
		return False

	def delete_meet(self, id: int):
		with self._connect() as conn:
			cursor = conn.cursor()

			cursor.execute('''
				DELETE FROM meets
				WHERE id = ?
			''', (id, ))

			conn.commit()

			return True
		
		return False
	
	def get_all_created_meets(self, user_id: int):
		with self._connect() as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()
			cursor.execute('''
				SELECT 
					meets.id AS meets_id,
					meets.title AS meets_title,
					meets.description AS meets_description,
					meets.field AS meets_field,
					meets.location AS meets_location, 
					meets.start_date AS meets_start_date,
					meets.start_time AS meets_start_time,
					meets.users_limit AS meets_users_limit,
					meets.created_by AS meets_created_by,
					COUNT(users_meets.users_id) AS user_count
				FROM meets
				LEFT JOIN users_meets
				ON users_meets.meets_id = meets.id
				WHERE meets.created_by = ?
				GROUP BY 
					meets.id,
					meets.title,
					meets.description,
					meets.field,
					meets.location, 
					meets.start_date,
					meets.start_time,
					meets.users_limit,
					meets.created_by
				ORDER BY meets.start_date DESC
		''', (user_id, ))
			
			meets = cursor.fetchall()
			meets_dict = convert_sqlite3rows_to_dict(meets)
			return meets_dict
		
	def get_meet_info_by_creator(self, user_id: int, meet_id: int):
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
					COUNT(users_meets.users_id) AS user_count
				FROM meets
				INNER JOIN users
				ON users.id = meets.created_by
				LEFT JOIN faculties
				ON users.faculty_id = faculties.id
				INNER JOIN users_meets
				ON users_meets.meets_id = meets.id
				WHERE meets.creator_id = ?
				AND meets.id = ?
			''', (user_id, meet_id))

			meet = cursor.fetchone()

			meet_dict = convert_sqlite3rows_to_dict(meet)

			return meet_dict
	
	def _ensure_unique_id(self, int_from = 100000000, int_to = 999999999) -> int:
		with self._connect() as conn: 
			cursor = conn.cursor()
			id = random.randint(int_from, int_to)
			
			while True: 
				cursor.execute('SELECT * FROM meets WHERE id = ?', (id, ))
				res = cursor.fetchone()

				if res is None:
					break
				else:
					id = random.randint(int_from, int_to)

			return id