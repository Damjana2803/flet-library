from models.user import User, Admin
from models.member import Member
from utils.global_state import global_state

def handle_login(email: str, password: str, login_type: str = "member"):
    """
    Handle login for both admin and member users
    
    Args:
        email: User email
        password: User password
        login_type: "admin" or "member"
    
    Returns:
        tuple: (success, user_data)
    """
    if login_type == "admin":
        return handle_admin_login(email, password)
    else:
        return handle_member_login(email, password)

def handle_admin_login(email: str, password: str):
    """Handle admin login"""
    # For now, use simple admin credentials
    # In production, this should use proper authentication
    admin_credentials = {
        "admin@biblioteka.rs": "admin123",
        "librarian@biblioteka.rs": "librarian123"
    }
    
    if email in admin_credentials and admin_credentials[email] == password:
        admin_data = {
            'id': 1,
            'username': email.split('@')[0],
            'email': email,
            'first_name': 'Admin',
            'last_name': 'Biblioteka',
            'role': 'admin',
            'is_admin': True,
            'permissions': ['books', 'members', 'loans', 'reports'],
            'is_active': True
        }
        global_state.set("user", admin_data)
        return True, admin_data
    
    return False, None

def handle_member_login(email: str, password: str):
    """Handle member login"""
    import hashlib
    
    # Get registered users from global state
    users = global_state.get("users", [])
    members = global_state.get("members", [])
    
    # Hash the provided password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Find the user with matching email and password
    for user in users:
        if user.get("email") == email and user.get("password_hash") == password_hash:
            # Find the corresponding member data
            member_id = user.get("member_id")
            member_data = None
            
            for member in members:
                if member.get("id") == member_id:
                    member_data = member
                    break
            
            if member_data:
                # Create user data for login using the actual member data
                login_data = {
                    'id': member_data.get('id'),
                    'first_name': member_data.get('first_name'),
                    'last_name': member_data.get('last_name'),
                    'email': member_data.get('email'),
                    'membership_number': member_data.get('membership_number'),
                    'membership_type': member_data.get('membership_type'),
                    'membership_status': member_data.get('membership_status'),
                    'current_loans': member_data.get('current_loans', 0),
                    'max_loans': member_data.get('max_loans', 5),
                    'is_admin': False
                }
                global_state.set("user", login_data)
                return True, login_data
    
    return False, None

# Legacy function for backward compatibility
def handle_login_legacy(email: str, password: str):
    user_model = User()
    user = user_model.login_user(email.lower(), password)
    
    if user['logged']:
        global_state.set_user(user)
        
    return user['logged']