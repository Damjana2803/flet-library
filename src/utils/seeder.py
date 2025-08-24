"""
Database Seeder for Library Management System

This module provides comprehensive seeding functionality for the library database.
It creates sample books, members, and admin users for development and testing.

Usage:
    - Automatically runs on first database initialization
    - Can be manually triggered if needed
    - Only seeds if database is empty or seeder hasn't run before

Features:
    - Creates admin user (admin@biblioteka.rs / admin123)
    - Creates sample members with realistic data
    - Creates sample books with various quantities (0, 1, 2+)
    - Creates sample loans and reservations
    - Tracks seeding status to prevent duplicate seeding
"""

import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import random

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect("database.db")

def check_if_seeded() -> bool:
    """Check if database has already been seeded"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if seeder_state table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='seeder_state'
        """)
        
        if not cursor.fetchone():
            # Create seeder_state table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS seeder_state (
                    id INTEGER PRIMARY KEY,
                    seeded BOOLEAN DEFAULT FALSE,
                    seeded_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute("INSERT INTO seeder_state (id, seeded) VALUES (1, FALSE)")
            conn.commit()
            conn.close()
            return False
        
        # Check if already seeded
        cursor.execute("SELECT seeded FROM seeder_state WHERE id = 1")
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else False
        
    except Exception as e:
        print(f"Error checking seeder state: {e}")
        return False

def mark_as_seeded():
    """Mark database as seeded"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE seeder_state SET seeded = TRUE, seeded_at = ? WHERE id = 1", 
                      (datetime.now().isoformat(),))
        conn.commit()
        conn.close()
        print("✅ Database marked as seeded")
    except Exception as e:
        print(f"Error marking as seeded: {e}")

def create_admin_user():
    """Create admin user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        admin_email = "admin@biblioteka.rs"
        admin_password = "admin123"
        password_hash = hashlib.sha256(admin_password.encode()).hexdigest()
        
        # Check if admin already exists
        cursor.execute("SELECT id FROM library_users WHERE email = ?", (admin_email,))
        if cursor.fetchone():
            print(f"✅ Admin user {admin_email} already exists")
            conn.close()
            return
        
        # Create admin user
        cursor.execute('''
            INSERT INTO library_users (email, password_hash, user_type, member_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (admin_email, password_hash, 'admin', None, datetime.now().isoformat(), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        print(f"✅ Admin user created: {admin_email} / {admin_password}")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")

def create_sample_members() -> List[int]:
    """Create sample members and return their IDs"""
    members_data = [
        {
            "first_name": "Damjana",
            "last_name": "Zubac",
            "email": "dada@gmail.com",
            "phone": "+381 60 123 4567",
            "address": "Bulevar oslobođenja 123, Novi Sad",
            "membership_number": "MEM001",
            "membership_type": "regular"
        },
        {
            "first_name": "Djordje",
            "last_name": "Zubac",
            "email": "djordje.zubac@w3-lab.com",
            "phone": "+381 60 987 6543",
            "address": "Zmaj Jovina 45, Novi Sad",
            "membership_number": "MEM002",
            "membership_type": "student"
        },
        {
            "first_name": "Ana",
            "last_name": "Petrović",
            "email": "ana.petrovic@gmail.com",
            "phone": "+381 60 555 1234",
            "address": "Dunavska 78, Novi Sad",
            "membership_number": "MEM003",
            "membership_type": "regular"
        },
        {
            "first_name": "Marko",
            "last_name": "Jovanović",
            "email": "marko.jovanovic@yahoo.com",
            "phone": "+381 60 777 8888",
            "address": "Bulevar Mihajla Pupina 12, Novi Sad",
            "membership_number": "MEM004",
            "membership_type": "senior"
        },
        {
            "first_name": "Jelena",
            "last_name": "Nikolić",
            "email": "jelena.nikolic@hotmail.com",
            "phone": "+381 60 444 5678",
            "address": "Futoška 34, Novi Sad",
            "membership_number": "MEM005",
            "membership_type": "student"
        },
        {
            "first_name": "Stefan",
            "last_name": "Đorđević",
            "email": "stefan.djordjevic@gmail.com",
            "phone": "+381 60 333 9999",
            "address": "Bulevar cara Lazara 67, Novi Sad",
            "membership_number": "MEM006",
            "membership_type": "regular"
        }
    ]
    
    member_ids = []
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for i, member_data in enumerate(members_data, 1):
            # Check if member already exists
            cursor.execute("SELECT id FROM library_members WHERE email = ?", (member_data["email"],))
            if cursor.fetchone():
                print(f"✅ Member {member_data['email']} already exists")
                continue
            
            # Set max loans based on membership type
            max_loans = 5  # Default for regular
            if member_data["membership_type"] == 'student':
                max_loans = 3
            elif member_data["membership_type"] == 'senior':
                max_loans = 7
            
            # Create member
            cursor.execute('''
                INSERT INTO library_members 
                (id, first_name, last_name, email, phone, address, membership_number,
                 membership_type, membership_status, membership_start_date, membership_end_date,
                 max_loans, current_loans, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                i, member_data["first_name"], member_data["last_name"], member_data["email"],
                member_data["phone"], member_data["address"], member_data["membership_number"],
                member_data["membership_type"], 'active', datetime.now().date().isoformat(),
                (datetime.now().date() + timedelta(days=365)).isoformat(),
                max_loans, 0, datetime.now().isoformat(), datetime.now().isoformat()
            ))
            
            member_ids.append(i)
            print(f"✅ Member created: {member_data['first_name']} {member_data['last_name']} ({member_data['email']})")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating members: {e}")
    
    return member_ids

def create_sample_books():
    """Create sample books with various quantities"""
    books_data = [
        # Books with 0 quantity (out of stock)
        {
            "title": "1984",
            "author": "Đordž Orvel",
            "isbn": "978-0451524935",
            "category": "Fiction",
            "publication_year": 1949,
            "publisher": "Signet Classic",
            "description": "Distopijski roman o totalitarnom društvu pod nadzorom.",
            "total_copies": 0,
            "available_copies": 0,
            "location": "Shelf A1"
        },
        {
            "title": "Veliki Getsbi",
            "author": "F. Skot Ficdžerald",
            "isbn": "978-0743273565",
            "category": "Fiction",
            "publication_year": 1925,
            "publisher": "Scribner",
            "description": "Priča o bogatom Džej Getsbiju i njegovoj ljubavi prema lepoj Dejzi Bjukanan.",
            "total_copies": 0,
            "available_copies": 0,
            "location": "Shelf A2"
        },
        
        # Books with 1 quantity (limited stock)
        {
            "title": "Ubijati pticu rugalicu",
            "author": "Harper Li",
            "isbn": "978-0446310789",
            "category": "Fiction",
            "publication_year": 1960,
            "publisher": "Grand Central Publishing",
            "description": "Priča o rasnoj nepravdi i gubitku nevinosti na američkom jugu.",
            "total_copies": 1,
            "available_copies": 1,
            "location": "Shelf B1"
        },
        {
            "title": "Gordost i predrasude",
            "author": "Džejn Ostin",
            "isbn": "978-0141439518",
            "category": "Fiction",
            "publication_year": 1813,
            "publisher": "Penguin Classics",
            "description": "Romantični roman o ponašanju koji prati emotivni razvoj Elizabet Benet.",
            "total_copies": 1,
            "available_copies": 1,
            "location": "Shelf B2"
        },
        {
            "title": "Lovac u žitu",
            "author": "Dž. D. Selindžer",
            "isbn": "978-0316769488",
            "category": "Fiction",
            "publication_year": 1951,
            "publisher": "Little, Brown and Company",
            "description": "Roman o tinejdžerskoj otuđenosti i gubitku nevinosti u Americi nakon Drugog svetskog rata.",
            "total_copies": 1,
            "available_copies": 1,
            "location": "Shelf B3"
        },
        
        # Books with multiple copies
        {
            "title": "Hobit",
            "author": "Dž. R. R. Tolkin",
            "isbn": "978-0547928241",
            "category": "Fantasy",
            "publication_year": 1937,
            "publisher": "Houghton Mifflin Harcourt",
            "description": "Fantastični roman o hobitovom putovanju da povrati patuljsko kraljevstvo.",
            "total_copies": 3,
            "available_copies": 3,
            "location": "Shelf C1"
        },
        {
            "title": "Gospodar prstenova",
            "author": "Dž. R. R. Tolkin",
            "isbn": "978-0547928210",
            "category": "Fantasy",
            "publication_year": 1954,
            "publisher": "Houghton Mifflin Harcourt",
            "description": "Epski fantastični roman o potrazi za uništavanjem moćnog prstena.",
            "total_copies": 2,
            "available_copies": 2,
            "location": "Shelf C2"
        },
        {
            "title": "Hari Poter i kamen mudraca",
            "author": "Dž. K. Rouling",
            "isbn": "978-0747532699",
            "category": "Fantasy",
            "publication_year": 1997,
            "publisher": "Bloomsbury",
            "description": "Prvi roman iz serije Hari Poter o mladom čarobnjaku.",
            "total_copies": 4,
            "available_copies": 4,
            "location": "Shelf C3"
        },
        {
            "title": "Alhemičar",
            "author": "Paulo Koeljo",
            "isbn": "978-0062315007",
            "category": "Fiction",
            "publication_year": 1988,
            "publisher": "HarperOne",
            "description": "Roman o mladom andaluzijskom pastiru koji sanja o pronalaženju svetskog blaga.",
            "total_copies": 2,
            "available_copies": 2,
            "location": "Shelf D1"
        },
        {
            "title": "Mali princ",
            "author": "Antoan de Sent Egziperi",
            "isbn": "978-0156013987",
            "category": "Fiction",
            "publication_year": 1943,
            "publisher": "Harcourt",
            "description": "Poezija o mladom princu koji poseti različite planete u svemiru.",
            "total_copies": 3,
            "available_copies": 3,
            "location": "Shelf D2"
        },
        
        # Non-fiction books
        {
            "title": "Sapiens: Kratka istorija čovečanstva",
            "author": "Juval Noa Harari",
            "isbn": "978-0062316097",
            "category": "History",
            "publication_year": 2011,
            "publisher": "Harper",
            "description": "Knjiga o istoriji ljudske evolucije i civilizacije.",
            "total_copies": 2,
            "available_copies": 2,
            "location": "Shelf E1"
        },
        {
            "title": "Umetnost rata",
            "author": "Sun Cu",
            "isbn": "978-0140439199",
            "category": "Military",
            "publication_year": -500,
            "publisher": "Penguin Classics",
            "description": "Drevni kineski tekst o vojnoj strategiji i taktici.",
            "total_copies": 1,
            "available_copies": 1,
            "location": "Shelf E2"
        },
        {
            "title": "Psihologija novca",
            "author": "Morgan Hausel",
            "isbn": "978-0857197689",
            "category": "Psychology",
            "publication_year": 2020,
            "publisher": "Harriman House",
            "description": "Vremenske lekcije o bogatstvu, pohlepi i sreći.",
            "total_copies": 2,
            "available_copies": 2,
            "location": "Shelf F1"
        }
    ]
    
    book_ids = []
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for i, book_data in enumerate(books_data, 1):
            # Check if book already exists
            cursor.execute("SELECT id FROM library_books WHERE isbn = ?", (book_data["isbn"],))
            if cursor.fetchone():
                print(f"✅ Book {book_data['title']} already exists")
                continue
            
            # Create book
            cursor.execute('''
                INSERT INTO library_books 
                (id, title, author, isbn, category, publication_year, publisher, description,
                 total_copies, available_copies, location, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                i, book_data["title"], book_data["author"], book_data["isbn"],
                book_data["category"], book_data["publication_year"], book_data["publisher"],
                book_data["description"], book_data["total_copies"], book_data["available_copies"],
                book_data["location"], datetime.now().isoformat(), datetime.now().isoformat()
            ))
            
            book_ids.append(i)
            print(f"✅ Book created: {book_data['title']} by {book_data['author']} ({book_data['total_copies']} copies)")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating books: {e}")
    
    return book_ids

def create_sample_loans_and_reservations(member_ids: List[int], book_ids: List[int]):
    """Create sample loans and reservations"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create some active loans
        loan_data = [
            (member_ids[0], book_ids[2], datetime.now().date() - timedelta(days=5), datetime.now().date() + timedelta(days=9)),  # Damjana borrowed Ubijati pticu rugalicu
            (member_ids[1], book_ids[3], datetime.now().date() - timedelta(days=3), datetime.now().date() + timedelta(days=11)),  # Djordje borrowed Gordost i predrasude
        ]
        
        for i, (member_id, book_id, loan_date, due_date) in enumerate(loan_data, 1):
            cursor.execute('''
                INSERT INTO library_loans 
                (id, book_id, member_id, loan_date, due_date, return_date, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                i, book_id, member_id, loan_date.isoformat(), due_date.isoformat(),
                None, 'active', datetime.now().isoformat(), datetime.now().isoformat()
            ))
            
            # Update book available copies
            cursor.execute("UPDATE library_books SET available_copies = available_copies - 1 WHERE id = ?", (book_id,))
            
            # Update member current loans
            cursor.execute("UPDATE library_members SET current_loans = current_loans + 1 WHERE id = ?", (member_id,))
            
            print(f"✅ Loan created: Member {member_id} borrowed book {book_id}")
        
        # Create some reservations
        reservation_data = [
            (member_ids[2], book_ids[0], datetime.now().date(), datetime.now().date() + timedelta(days=7)),  # Ana reserved 1984
            (member_ids[3], book_ids[1], datetime.now().date(), datetime.now().date() + timedelta(days=7)),  # Marko reserved Veliki Getsbi
        ]
        
        for i, (member_id, book_id, reservation_date, expiry_date) in enumerate(reservation_data, 1):
            cursor.execute('''
                INSERT INTO library_reservations 
                (id, book_id, member_id, reservation_date, expiry_date, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                i, book_id, member_id, reservation_date.isoformat(), expiry_date.isoformat(),
                'active', datetime.now().isoformat(), datetime.now().isoformat()
            ))
            
            print(f"✅ Reservation created: Member {member_id} reserved book {book_id}")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating loans and reservations: {e}")

def create_member_users(member_ids: List[int]):
    """Create user accounts for members"""
    member_emails = [
        "dada@gmail.com",
        "djordje.zubac@w3-lab.com", 
        "ana.petrovic@gmail.com",
        "marko.jovanovic@yahoo.com",
        "jelena.nikolic@hotmail.com",
        "stefan.djordjevic@gmail.com"
    ]
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for i, email in enumerate(member_emails):
            if i >= len(member_ids):
                break
                
            # Check if user already exists
            cursor.execute("SELECT id FROM library_users WHERE email = ?", (email,))
            if cursor.fetchone():
                print(f"✅ User {email} already exists")
                continue
            
            # Create user with default password (email prefix + 123)
            password = email.split('@')[0] + "123"
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute('''
                INSERT INTO library_users (email, password_hash, user_type, member_id, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (email, password_hash, 'member', member_ids[i], datetime.now().isoformat(), datetime.now().isoformat()))
            
            print(f"✅ User created: {email} / {password}")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating member users: {e}")

def run_seeder():
    """Main seeder function"""
    print("🌱 Starting database seeder...")
    
    # Check if already seeded
    if check_if_seeded():
        print("✅ Database already seeded, skipping...")
        return
    
    print("📚 Creating admin user...")
    create_admin_user()
    
    print("👥 Creating sample members...")
    member_ids = create_sample_members()
    
    print("📖 Creating sample books...")
    book_ids = create_sample_books()
    
    print("🔗 Creating sample loans and reservations...")
    create_sample_loans_and_reservations(member_ids, book_ids)
    
    print("👤 Creating member user accounts...")
    create_member_users(member_ids)
    
    # Mark as seeded
    mark_as_seeded()
    
    print("🎉 Database seeding completed successfully!")
    print("\n📋 Seeder Summary:")
    print("✅ Admin user: admin@biblioteka.rs / admin123")
    print("✅ 6 sample members with user accounts")
    print("✅ 13 sample books (0, 1, 2+ copies)")
    print("✅ 2 active loans")
    print("✅ 2 active reservations")
    print("\n🔑 Member Login Credentials:")
    print("- dada@gmail.com / dada123")
    print("- djordje.zubac@w3-lab.com / djordje.zubac123")
    print("- ana.petrovic@gmail.com / ana.petrovic123")
    print("- marko.jovanovic@yahoo.com / marko.jovanovic123")
    print("- jelena.nikolic@hotmail.com / jelena.nikolic123")
    print("- stefan.djordjevic@gmail.com / stefan.djordjevic123")

if __name__ == "__main__":
    run_seeder()
