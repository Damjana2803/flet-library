import re
from models.user import User

def handle_register(email: str, name: str, password: str, faculty: str) -> bool:
	from models.faculty import Faculty
	user_model = User()
	errors = []

	if email == '':
		errors.append({ 'field': 'email', 'message': 'E-adresa je obavezno polje' })
	
	elif re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is None:
		errors.append({ 'field': 'email', 'message': 'Unešena je nevalidna e-adresa' })

	if name == '':
		errors.append({ 'field': 'name', 'message': 'Ime je obavezno polje' })

	if len(password) < 6:
		errors.append({ 'field': 'password', 'message': 'Lozinka mora sadržati barem 6 karaktera' })


	faculty_model = Faculty()
	faculty_res = faculty_model.find_if_faculty_exists(faculty)

	if faculty is None:
		errors.append({ 'field': 'faculty', 'message': 'Fakultet je obavezno polje' })
	elif faculty_res is None:
		errors.append({ 'field': 'faculty', 'message': 'Fakultet sa tim imenom ne postoji' })

	if len(errors):
		return {
			'success': False,
			'errors': errors
		}
	
	registered_successfully = user_model.create_user(name, email, password, faculty_res)
	
	if not registered_successfully:
		errors.append({ 'field': 'email', 'message': 'Ova e-adresa je već u upotrebi' })

	return {
		'success': registered_successfully,
		'errors': errors
	}
