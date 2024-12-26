from models.user import User

async def get_all_users():
	user_model = User()

	users = user_model.get_all_users()

	return users
