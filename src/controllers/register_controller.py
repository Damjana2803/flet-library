from models.user import User

def handle_register(email: str, name: str, password: str, faculty: str) -> bool:
	user_model = User()
	registered_successfully: bool = user_model.create_user(name, email, password, faculty)
	
	
	del user_model
	return registered_successfully
