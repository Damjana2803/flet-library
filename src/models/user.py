import sqlite3, random, os
from hashlib import sha256
from dotenv import load_dotenv
from models.faculty import Faculty
from utils.helper_func import convert_sqlite3rows_to_dict
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

load_dotenv()

@dataclass
class Admin:
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    password_hash: str = ""
    first_name: str = ""
    last_name: str = ""
    role: str = "admin"  # admin, librarian, assistant
    permissions: list = None
    is_active: bool = True
    last_login: datetime = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.permissions is None:
            self.permissions = ["books", "members", "loans", "reports"]
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'permissions': self.permissions,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            username=data.get('username', ''),
            email=data.get('email', ''),
            password_hash=data.get('password_hash', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            role=data.get('role', 'admin'),
            permissions=data.get('permissions', ["books", "members", "loans", "reports"]),
            is_active=data.get('is_active', True),
            last_login=datetime.fromisoformat(data['last_login']) if data.get('last_login') else None,
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions
    
    def update_last_login(self):
        self.last_login = datetime.now()
        self.updated_at = datetime.now()

class User: 
	def __init__(self, db_path = os.getenv('DB_NAME')):
		self.db_path = db_path

	def _connect(self):
		return sqlite3.connect(self.db_path)

	def create_user(self, name: str, email: str, password: str, faculty: int) -> bool:
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
			
			if user is None:
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

			if res is None:
				return {
					'logged': False
				}
			
			user = self.get_user_by_email(email)

			Session().create_session(user_id = user['id'])
			
			user['logged'] = True
			return user

	def get_all_users(self):
		with self._connect() as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()

			cursor.execute('''
				SELECT 
					users.id AS id,
					users.name AS name,
					users.email AS email,
					users.is_admin AS is_admin,
					faculties.name AS faculty
				FROM users
				LEFT JOIN faculties
				ON faculties.id = users.faculty_id
			''')

			users = cursor.fetchall()

			return convert_sqlite3rows_to_dict(users)

	def edit_user(self, user_id: int, name: str, faculty: int):
		with self._connect() as conn:
			cursor = conn.cursor()

			cursor.execute('''
				UPDATE users
				SET name = ?, faculty = ?
				WHERE id = ?
			''', (name, faculty, user_id))

			conn.commit()

			return True
		
		return False

	
	def delete_user(self, user_id: int):
		with self._connect() as conn:
			cursor = conn.cursor()

			cursor.execute('''
				DELETE FROM users
				WHERE id = ?
			''', (user_id, ))

			conn.commit()

			return True

		return False

	def _hash_password(self, password: str) -> str:
		return sha256(password.encode('utf-8')).hexdigest()
	
	def _ensure_unique_id(self, int_from = 100000000, int_to = 999999999) -> int:
		with self._connect() as conn: 
			cursor = conn.cursor()
			id = random.randint(int_from, int_to)
			while True: 
				cursor.execute('SELECT * FROM users WHERE id = ?', (id, ))
				res = cursor.fetchone()

				if res is None:
					break
				else:
					id = random.randint(int_from, int_to)

			return id

	