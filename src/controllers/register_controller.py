import re
from models.user import User
from utils.global_state import global_state
from models.member import Member
from datetime import datetime
import hashlib

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

def handle_member_register(full_name: str, email: str, password: str, phone: str, address: str, membership_type: str) -> tuple[bool, str]:
    """
    Handle member registration
    Returns: (success: bool, message: str)
    """
    try:
        # Basic validation
        if not full_name:
            return False, "Ime i prezime je obavezno polje"
        if not email:
            return False, "E-adresa je obavezno polje"
        if not password:
            return False, "Lozinka je obavezno polje"
        if not phone:
            return False, "Broj telefona je obavezno polje"
        if not address:
            return False, "Adresa je obavezno polje"
        if not membership_type:
            return False, "Tip članstva je obavezno polje"
        
        if len(password) < 6:
            return False, "Lozinka mora imati najmanje 6 karaktera"
        
        # Check if email already exists
        existing_members = global_state.members
        # Convert existing members to Member objects if they're dictionaries
        member_objects = []
        for member_data in existing_members:
            if isinstance(member_data, dict):
                member_objects.append(Member.from_dict(member_data))
            else:
                member_objects.append(member_data)
        
        if any(member.email == email for member in member_objects):
            return False, "E-adresa već postoji"
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Set max loans based on membership type
        max_loans = 5  # Default for regular
        if membership_type == 'student':
            max_loans = 3
        elif membership_type == 'senior':
            max_loans = 7
        
        # Split full name into first and last name
        name_parts = full_name.strip().split(' ', 1)
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        # Create new member
        new_member = Member(
            id=len(existing_members) + 1,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            membership_number=f"MEM{len(existing_members) + 1:03d}",
            membership_type=membership_type,
            membership_status="active",
            membership_start_date=datetime.now(),
            membership_end_date=datetime.now().replace(year=datetime.now().year + 1),
            max_loans=max_loans,
            created_at=datetime.now()
        )
        
        # Store member data (in real app, save to database)
        # Convert Member object to dictionary for storage
        member_dict = new_member.to_dict()
        existing_members.append(member_dict)
        global_state.members = existing_members
        
        # Also store user credentials for login
        users = global_state.users
        users.append({
            "email": email,
            "password_hash": password_hash,
            "user_type": "member",
            "member_id": new_member.id
        })
        global_state.users = users
        global_state.save_data_to_file()
        
        return True, "Registracija uspešna! Možete se prijaviti."
        
    except Exception as e:
        return False, f"Greška prilikom registracije: {str(e)}"

def handle_register_legacy(name: str, email: str, password: str, faculty: str) -> tuple[bool, str]:
    """
    Legacy register function for backward compatibility
    """
    return handle_member_register(name, "", email, password, "", "", "regular")
