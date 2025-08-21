import hashlib
from utils.library_db import authenticate_user, create_user
from utils.db import db_init
from models.session import Session
from datetime import datetime, timedelta

def login_user(email: str, password: str) -> tuple[bool, str, dict]:
    """
    Authenticate a user
    Returns: (success: bool, message: str, user_data: dict)
    """
    try:
        if not email or not password:
            return False, "Molimo unesite email i lozinku", {}
        
        # Hash the password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Try to authenticate with library database first
        user = authenticate_user(email, password_hash)
        
        if user:
            # User found in library database
            user_data = {
                'id': user['id'],
                'email': user['email'],
                'user_type': user['user_type'],
                'member_id': user['member_id'],
                'is_admin': user['user_type'] == 'admin'
            }
            return True, "Uspešna prijava", user_data
        
        # If not found in library database, try legacy Athena database
        # This maintains backward compatibility
        conn = db_init()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, email, is_admin FROM users WHERE email = ? AND password = ?", 
                      (email, password_hash))
        user_result = cursor.fetchone()
        conn.close()
        
        if user_result:
            user_data = {
                'id': user_result[0],
                'name': user_result[1],
                'email': user_result[2],
                'is_admin': bool(user_result[3]),
                'user_type': 'admin' if user_result[3] else 'user'
            }
            return True, "Uspešna prijava", user_data
        
        return False, "Pogrešan email ili lozinka", {}
        
    except Exception as e:
        return False, f"Greška pri prijavi: {str(e)}", {}

def register_user(email: str, password: str, first_name: str, last_name: str, 
                 phone: str, address: str, membership_type: str) -> tuple[bool, str]:
    """
    Register a new user
    Returns: (success: bool, message: str)
    """
    try:
        if not all([email, password, first_name, last_name, phone, address, membership_type]):
            return False, "Sva polja su obavezna"
        
        if len(password) < 6:
            return False, "Lozinka mora imati najmanje 6 karaktera"
        
        # Hash the password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Generate membership number
        from utils.library_db import get_all_members
        members = get_all_members()
        membership_number = f"MEM{len(members) + 1:03d}"
        
        # Add member to database
        from utils.library_db import add_member
        success, message = add_member(first_name, last_name, email, phone, address, membership_number, membership_type)
        
        if not success:
            return False, message
        
        # Get the member ID
        members = get_all_members()
        member = next((m for m in members if m['email'] == email), None)
        
        if not member:
            return False, "Greška pri kreiranju člana"
        
        # Create user account
        success, message = create_user(email, password_hash, 'member', member['id'])
        
        if not success:
            return False, message
        
        return True, "Registracija uspešna! Možete se prijaviti sa vašim podacima."
        
    except Exception as e:
        return False, f"Greška pri registraciji: {str(e)}"

def create_session(user_id: int, user_type: str = 'member') -> Session:
    """
    Create a new session for the user
    Returns: Session object
    """
    try:
        # Generate session token
        import secrets
        token = secrets.token_urlsafe(32)
        
        # Set session expiry (30 days)
        valid_until = datetime.now() + timedelta(days=30)
        
        # Save session to database
        conn = db_init()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sessions (token, is_active, valid_until, users_id)
            VALUES (?, ?, ?, ?)
        ''', (token, 1, valid_until.isoformat(), user_id))
        
        conn.commit()
        conn.close()
        
        return Session(
            id=1,  # This will be set by the database
            token=token,
            is_active=True,
            valid_until=valid_until,
            user_id=user_id
        )
        
    except Exception as e:
        print(f"Greška pri kreiranju sesije: {str(e)}")
        return None

def validate_session(token: str) -> tuple[bool, dict]:
    """
    Validate a session token
    Returns: (is_valid: bool, user_data: dict)
    """
    try:
        conn = db_init()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.is_active, s.valid_until, u.id, u.name, u.email, u.is_admin
            FROM sessions s
            JOIN users u ON s.users_id = u.id
            WHERE s.token = ?
        ''', (token,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return False, {}
        
        is_active, valid_until_str, user_id, name, email, is_admin = result
        
        if not is_active:
            return False, {}
        
        valid_until = datetime.fromisoformat(valid_until_str)
        if datetime.now() > valid_until:
            return False, {}
        
        user_data = {
            'id': user_id,
            'name': name,
            'email': email,
            'is_admin': bool(is_admin),
            'user_type': 'admin' if is_admin else 'user'
        }
        
        return True, user_data
        
    except Exception as e:
        print(f"Greška pri validaciji sesije: {str(e)}")
        return False, {}

def logout_user(token: str) -> bool:
    """
    Logout user by invalidating session
    Returns: success: bool
    """
    try:
        conn = db_init()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE sessions 
            SET is_active = 0
            WHERE token = ?
        ''', (token,))
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Greška pri odjavi: {str(e)}")
        return False