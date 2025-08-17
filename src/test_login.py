import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.global_state import global_state
import hashlib

def test_login():
    print("=== TEST LOGIN ===")
    
    # Check if data is loaded
    print(f"Users in global state: {len(global_state.users)}")
    print(f"Members in global state: {len(global_state.members)}")
    
    # Test with known user
    test_email = "dami@gmail.com"
    test_password = "dacika123"  # Actual password
    
    # Hash password
    password_hash = hashlib.sha256(test_password.encode()).hexdigest()
    print(f"Test email: {test_email}")
    print(f"Test password hash: {password_hash}")
    
    # Check users
    for user in global_state.users:
        print(f"User: {user}")
        if user.get("email") == test_email:
            print(f"Found user with email {test_email}")
            if user.get("password_hash") == password_hash:
                print("Password matches!")
                return True
            else:
                print(f"Password doesn't match. Expected: {password_hash}, Got: {user.get('password_hash')}")
    
    print("User not found or password doesn't match")
    return False

if __name__ == "__main__":
    test_login()
