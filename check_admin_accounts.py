#!/usr/bin/env python3
"""
Script to check available administrator accounts
"""

import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def check_admin_accounts():
    """Check what administrator accounts are available"""
    print("🔍 Checking administrator accounts...")
    print("=" * 50)
    
    try:
        # Connect to database
        conn = sqlite3.connect(os.getenv('DB_NAME'))
        cursor = conn.cursor()
        
        # Check library users (new system)
        print("📚 Library System Users:")
        cursor.execute("SELECT email, user_type, member_id FROM library_users")
        library_users = cursor.fetchall()
        
        if library_users:
            for user in library_users:
                print(f"  - {user[0]} (Type: {user[1]}, Member ID: {user[2]})")
        else:
            print("  No library users found")
        
        # Check legacy Athena users
        print("\n🏛️ Legacy Athena Users:")
        cursor.execute("SELECT name, email, is_admin FROM users")
        athena_users = cursor.fetchall()
        
        if athena_users:
            for user in athena_users:
                admin_status = "ADMIN" if user[2] else "User"
                print(f"  - {user[0]} ({user[1]}) - {admin_status}")
        else:
            print("  No Athena users found")
        
        # Check if we have any admin users
        print("\n👑 Administrator Accounts:")
        admin_found = False
        
        # Check library users for admin type
        cursor.execute("SELECT email FROM library_users WHERE user_type = 'admin'")
        library_admins = cursor.fetchall()
        
        if library_admins:
            admin_found = True
            for admin in library_admins:
                print(f"  ✅ Library Admin: {admin[0]}")
        
        # Check Athena users for admin flag
        cursor.execute("SELECT name, email FROM users WHERE is_admin = 1")
        athena_admins = cursor.fetchall()
        
        if athena_admins:
            admin_found = True
            for admin in athena_admins:
                print(f"  ✅ Athena Admin: {admin[0]} ({admin[1]})")
        
        if not admin_found:
            print("  ⚠️  No administrator accounts found!")
            print("  💡 You may need to create an admin account")
        
        conn.close()
        
        print("\n" + "=" * 50)
        print("💡 Login Instructions:")
        print("  - For Library System: Use email and password")
        print("  - For Legacy Athena: Use email and password")
        print("  - Default Athena admin: admin@athena.com / admin")
        
    except Exception as e:
        print(f"❌ Error checking accounts: {e}")

if __name__ == "__main__":
    check_admin_accounts()
