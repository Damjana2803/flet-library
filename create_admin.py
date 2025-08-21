#!/usr/bin/env python3
"""
Script to create an administrator account for the library system
"""

import sqlite3
import os
import hashlib
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def create_admin_account():
    """Create an administrator account for the library system"""
    print("🔧 Creating administrator account...")
    print("=" * 50)
    
    try:
        # Connect to database
        conn = sqlite3.connect(os.getenv('DB_NAME'))
        cursor = conn.cursor()
        
        # Admin credentials
        admin_email = "admin@biblioteka.rs"
        admin_password = "admin123"
        password_hash = hashlib.sha256(admin_password.encode()).hexdigest()
        
        # Check if admin already exists
        cursor.execute("SELECT id FROM library_users WHERE email = ?", (admin_email,))
        if cursor.fetchone():
            print(f"⚠️  Admin account {admin_email} already exists!")
            conn.close()
            return
        
        # Create admin user
        cursor.execute('''
            INSERT INTO library_users (email, password_hash, user_type, member_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (admin_email, password_hash, 'admin', None, datetime.now().isoformat(), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        print("✅ Administrator account created successfully!")
        print(f"📧 Email: {admin_email}")
        print(f"🔑 Password: {admin_password}")
        print("\n💡 You can now log in as administrator!")
        
    except Exception as e:
        print(f"❌ Error creating admin account: {e}")

if __name__ == "__main__":
    create_admin_account()
