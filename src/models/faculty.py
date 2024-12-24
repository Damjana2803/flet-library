import sqlite3, os
from dotenv import load_dotenv

load_dotenv()

class Faculty:
	def __init__(self, db_path = os.getenv('DB_NAME')):
		self.db_path = db_path

	def _connect(self):
		return sqlite3.connect(self.db_path)
	
	def find_if_faculty_exists(self, name: str):
		with self._connect() as conn:
			cursor = conn.cursor()

			cursor.execute('SELECT id FROM faculties WHERE name = ?', (name, ))
			res = cursor.fetchone()

			return res