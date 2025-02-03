from utils.global_state import global_state
from models.meet import Meet
from models.usermeet import UserMeet
from datetime import datetime

async def handle_create_meet(title: str, description: str, field: str, location: str, start_date, start_time, users_limit: int):	
	user = global_state.get_user()
	user_id = user['id']
	errors = []
	meets_model = Meet()

	if title == '':
		errors.append({ 'field': 'title', 'message': 'Naslov Simpozijuma je obavezno polje' })

	if field == '':
		errors.append({ 'field': 'field', 'message': 'Naučno polje je obavezno' })

	if location == '':
		errors.append({ 'field': 'location', 'message': 'Lokacija je obavezna' })

	try:
		combined_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
		if combined_datetime < datetime.now():
			errors.append({ 'field': 'date', 'message': 'Datum i vreme ne mogu biti u prošlosti' })
	except ValueError:
		errors.append({ 'field': 'date', 'message': 'Neispravan format datuma ili vremena' })

	if users_limit == '' or int(users_limit) == 0:
		errors.append({ 'field': 'limit', 'message': 'Mora postojati bar jedno slobodno mesto' })

	if len(errors):
		return {
			'success': False,
			'errors': errors
		}
	
	return meets_model.create_meet(title, description, field, location, start_date, start_time, users_limit, user_id)
		
async def handle_get_meet(id: int):
	meet_model = Meet()

	meet = meet_model.get_meet_by_id(id)
	return meet

async def handle_get_all_valid_meets(search: str):
	user = global_state.get_user()
	user_id = user['id']
	
	meet_model = Meet()

	return meet_model.get_all_valid_meets(user_id, search)

# TODO: change this to support retrieving other parameters (comment and rating...)
async def handle_check_if_user_is_signed(user_id: int, meet_id: int):
	user_meet_model = UserMeet()

	return user_meet_model.check_if_user_is_signed(user_id, meet_id)

async def handle_get_users_in_meet(meet_id: int):
	user_meet_model = UserMeet()

	return user_meet_model.get_users_in_meet( meet_id)

async def handle_toggle_join_user(user_id: int, meet_id: int):
	user_meet_model = UserMeet()

	return user_meet_model.toggle_join_user(user_id, meet_id)

async def handle_get_all_created_meets(user_id: int, search: str):
	meet_model = Meet()

	created_meets = meet_model.get_all_created_meets(user_id, search)

	if len(created_meets) == 1:
		if created_meets[0]['meets_id'] is None:
			return []

	return created_meets

async def handle_get_all_joined_meets(user_id: int):
	user_meet_model = UserMeet()
	
	return user_meet_model.get_all_joined_meets(user_id)

async def handle_add_comment(user_id: int, meet_id: int, rating: int, comment: str):
	user_meet_model = UserMeet()

	success = user_meet_model.add_comment(user_id, meet_id, rating, comment)

	return success
