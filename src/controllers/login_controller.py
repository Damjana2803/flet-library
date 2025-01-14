from models.user import User
from utils.global_state import global_state

def handle_login(email: str, password: str):
	user_model = User()

	user = user_model.login_user(email.lower(), password)
	
	if user['logged']:
		global_state.set_user(user)
		
	return user['logged']