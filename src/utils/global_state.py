from models.session import Session
import json
import os

class GlobalState:
	def __init__(self):
		self.user = {}
		# Initialize data lists first
		self.books = []
		self.members = []
		self.loans = []
		self.reservations = []
		self.users = []
		self.load_data_from_file()  # Load data from file
		self._check_if_logged_in()

	def set_init(self):
		self.user = {} 

	def set_user(self, user_data: dict):
		self.user = user_data

	def get_user(self):
		return self.user
	
	def get(self, key: str, default=None):
		"""Get a value from global state by key"""
		if not hasattr(self, key):
			return default
		return getattr(self, key, default)
	
	def set(self, key: str, value):
		"""Set a value in global state by key"""
		setattr(self, key, value)
		# Auto-save to file when data is updated
		self.save_data_to_file()
	
	def get_token(self) -> str | None:
		if 'token' not in self.user:
			return None
		
		return self.user['token']

	def _check_if_logged_in(self):
		token = Session().get_session_token_from_file()

		if token:
			self.user = Session().get_user_by_token(token)	
			self.user['token'] = token
	
	def save_data_to_file(self):
		"""Save all data to JSON file"""
		data = {
			'books': self.books,
			'members': self.members,
			'loans': self.loans,
			'reservations': self.reservations,
			'users': self.users
		}
		
		# Create storage directory if it doesn't exist
		os.makedirs('storage', exist_ok=True)
		
		with open('storage/library_data.json', 'w', encoding='utf-8') as f:
			json.dump(data, f, ensure_ascii=False, indent=2)
	
	def load_data_from_file(self):
		"""Load all data from JSON file"""
		file_path = 'storage/library_data.json'
		
		if os.path.exists(file_path):
			try:
				with open(file_path, 'r', encoding='utf-8') as f:
					data = json.load(f)
					self.books = data.get('books', [])
					self.members = data.get('members', [])
					self.loans = data.get('loans', [])
					self.reservations = data.get('reservations', [])
					self.users = data.get('users', [])
			except Exception as e:
				print(f"Error loading data: {e}")
				# Initialize with empty lists if loading fails
				self.books = []
				self.members = []
				self.loans = []
				self.reservations = []
				self.users = []
		else:
			# Initialize with empty lists if file doesn't exist
			self.books = []
			self.members = []
			self.loans = []
			self.reservations = []
			self.users = []

global_state = GlobalState()