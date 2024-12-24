from utils.global_state import global_state
from models.meet import Meet
from models.usermeet import UserMeet

async def handle_create_meet(title: str, description: str, field: str, location: str, start_date, start_time, users_limit: int):	
	user = global_state.get_user()
	user_id = user['id']

	meets_model = Meet()

	return meets_model.create_meet(title, description, field, location, start_date, start_time, users_limit, user_id)
		
async def handle_get_meet(id: int):
	meet_model = Meet()

	meet = meet_model.get_meet_by_id(id)
	return meet

async def handle_get_all_valid_meets():
	user = global_state.get_user()
	user_id = user['id']
	
	meet_model = Meet()

	return meet_model.get_all_valid_meets(user_id)

async def handle_check_if_user_is_signed(user_id: int, meet_id: int):
	user_meet_model = UserMeet()

	return user_meet_model.check_if_user_is_signed(user_id, meet_id)

async def handle_toggle_join_user(user_id: int, meet_id: int):

	user_meet_model = UserMeet()

	return user_meet_model.toggle_join_user(user_id, meet_id)

async def handle_get_all_created_meets(user_id: int):
	meet_model = Meet()

	return meet_model.get_all_created_meets(user_id)