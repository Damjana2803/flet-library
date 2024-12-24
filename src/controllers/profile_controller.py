from models.session import Session
from utils.global_state import global_state

def handle_logout():
	token = global_state.get_token()
	session_model = Session()

	try:
		session_model.delete_session(token)
	except Exception as e:
		pass
	finally:
		if global_state.get_token():
			session_model.remove_session()