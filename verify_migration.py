#!/usr/bin/env python3
"""
Script to verify that the data migration from JSON to SQLite was successful
"""

import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def verify_migration():
    """Verify that all data was migrated correctly"""
    print("🔍 Verifying data migration from JSON to SQLite...")
    print("=" * 50)
    
    try:
        # Connect to database
        conn = sqlite3.connect(os.getenv('DB_NAME'))
        cursor = conn.cursor()
        
        # Check books
        cursor.execute("SELECT COUNT(*) FROM library_books")
        book_count = cursor.fetchone()[0]
        print(f"📚 Books in database: {book_count}")
        
        cursor.execute("SELECT title, author, isbn FROM library_books LIMIT 3")
        books = cursor.fetchall()
        print("Sample books:")
        for book in books:
            print(f"  - {book[0]} by {book[1]} (ISBN: {book[2]})")
        
        # Check members
        cursor.execute("SELECT COUNT(*) FROM library_members")
        member_count = cursor.fetchone()[0]
        print(f"\n👥 Members in database: {member_count}")
        
        cursor.execute("SELECT first_name, last_name, email, membership_type FROM library_members LIMIT 3")
        members = cursor.fetchall()
        print("Sample members:")
        for member in members:
            print(f"  - {member[0]} {member[1]} ({member[2]}) - {member[3]}")
        
        # Check loans
        cursor.execute("SELECT COUNT(*) FROM library_loans")
        loan_count = cursor.fetchall()[0]
        print(f"\n📖 Loans in database: {loan_count}")
        
        # Check users
        cursor.execute("SELECT COUNT(*) FROM library_users")
        user_count = cursor.fetchone()[0]
        print(f"👤 Users in database: {user_count}")
        
        # Check reservations
        cursor.execute("SELECT COUNT(*) FROM library_reservations")
        reservation_count = cursor.fetchone()[0]
        print(f"📅 Reservations in database: {reservation_count}")
        
        # Legacy tables (Athena system)
        cursor.execute("SELECT COUNT(*) FROM users")
        legacy_user_count = cursor.fetchone()[0]
        print(f"\n🏛️ Legacy Athena users: {legacy_user_count}")
        
        cursor.execute("SELECT COUNT(*) FROM faculties")
        faculty_count = cursor.fetchone()[0]
        print(f"🏛️ Legacy Athena faculties: {faculty_count}")
        
        conn.close()
        
        print("\n" + "=" * 50)
        print("✅ Migration verification completed!")
        print(f"📊 Summary:")
        print(f"   - Books: {book_count}")
        print(f"   - Members: {member_count}")
        print(f"   - Loans: {loan_count}")
        print(f"   - Users: {user_count}")
        print(f"   - Reservations: {reservation_count}")
        
        if book_count > 0 and member_count > 0:
            print("🎉 Migration appears to be successful!")
        else:
            print("⚠️  Some data may be missing from migration")
            
    except Exception as e:
        print(f"❌ Error during verification: {e}")

if __name__ == "__main__":
    verify_migration()
