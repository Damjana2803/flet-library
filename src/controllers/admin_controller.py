from models.user import User
from models.faculty import Faculty
from models.meet import Meet

async def get_all_users():
	user_model = User()

	users = user_model.get_all_users()

	return users

async def edit_user(user_id: int, name: str, faculty: str):
	user_model = User()
	faculty_model = Faculty()
	
	errors = []

	faculty_res = faculty_model.find_if_faculty_exists(faculty)

	if faculty is None:
		errors.append({ 'field': 'faculty', 'message': 'Fakultet je obavezno polje' })

	if len(errors):
		return {
			'success': False,
			'errors': errors
		}
	
	edited_successfully = user_model.edit_user(user_id, name, faculty_res)

	if not edited_successfully:
		errors.append({ 'field': 'name', 'message': 'Neočekivana greška' })

	return {
		'success': edited_successfully,
		'errors': errors
	}
	
async def delete_user(user_id: int):
	user_model = User()
	errors = []

	deleted_successfully = user_model.delete_user(user_id)

	return deleted_successfully

async def handle_get_all_meets():
	meet_model = Meet()

	meets = meet_model.get_all_meets()

	return meets

async def edit_meet(meet_id: int, title: str, description: str):
	meet_model = Meet()

	errors = []

	if not title:
		errors.append({'field': 'title', 'message': 'Naslov mora postojati'})

	if len(errors):
		return {
			'success': False,
			'errors': errors
		}
	
	edited_successfully = meet_model.edit_meet(meet_id, title, description)

	if not edited_successfully:
		errors.append({ 'field': 'name', 'message': 'Neočekivana greška' })

	return {
		'success': edited_successfully,
		'errors': errors
	}
	

async def delete_meet(meet_id: int):
	meet_model = Meet()

	deleted_successfully = meet_model.delete_meet(meet_id)

	return deleted_successfully