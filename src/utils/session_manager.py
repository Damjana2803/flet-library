"""
Simple session manager for storing user data
"""

# Global variable to store current user data
_current_user = None

def set_current_user(user_data):
    """Set the current user data"""
    global _current_user
    _current_user = user_data
    print(f"Session: User logged in - {user_data.get('email', 'Unknown')}")

def get_current_user():
    """Get the current user data"""
    global _current_user
    return _current_user

def clear_current_user():
    """Clear the current user data (logout)"""
    global _current_user
    if _current_user:
        print(f"Session: User logged out - {_current_user.get('email', 'Unknown')}")
    _current_user = None

def is_logged_in():
    """Check if user is logged in"""
    return _current_user is not None

def is_admin():
    """Check if current user is admin"""
    return _current_user and _current_user.get('is_admin', False)
