import hashlib

def test_simple_login():
    print("=== SIMPLE LOGIN TEST ===")
    
    # Test credentials
    email = "dami@gmail.com"
    password = "dacika123"
    
    # Hash password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"Password hash: {password_hash}")
    
    # Check if it matches stored hash
    stored_hash = "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"
    print(f"Stored hash: {stored_hash}")
    print(f"Match: {password_hash == stored_hash}")
    
    if password_hash == stored_hash:
        print("✅ LOGIN SHOULD WORK!")
        return True
    else:
        print("❌ LOGIN WON'T WORK!")
        return False

if __name__ == "__main__":
    test_simple_login()
