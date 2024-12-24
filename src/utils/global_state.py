from models.session import Session

class GlobalState:
	def __init__(self):
		self.user = {} 
		self._check_if_logged_in()

	def set_init(self):
		self.user = {} 

	def set_user(self, user_data: dict):
		self.user = user_data

	def get_user(self):
		return self.user
	
	def get_token(self) -> str | None:
		if 'token' not in self.user:
			return None
		
		return self.user['token']

	def _check_if_logged_in(self):
		token = Session().get_session_token_from_file()

		if token:
			self.user = Session().get_user_by_token(token)	
			self.user['token'] = token

global_state = GlobalState()