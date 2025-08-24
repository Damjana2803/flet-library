import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Get a database connection"""
    db_name = os.getenv('DB_NAME')
    if not db_name:
        db_name = "flet-library.db"
    
    # If running from src directory, go up one level to find the database
    if os.path.exists(os.path.join(os.getcwd(), '..', db_name)):
        db_path = os.path.join(os.getcwd(), '..', db_name)
    else:
        db_path = db_name
    
    print(f"🔗 LIBRARY_DB: Connecting to database: {db_path}")
    return sqlite3.connect(db_path)

# Book operations
def get_all_books() -> List[Dict]:
    """Get all books from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, title, author, isbn, category, publication_year, publisher, 
               description, total_copies, available_copies, location, status, created_at
        FROM library_books
        ORDER BY title
    ''')
    
    books = []
    for row in cursor.fetchall():
        books.append({
            'id': row[0],
            'title': row[1],
            'author': row[2],
            'isbn': row[3],
            'category': row[4],
            'publication_year': row[5],
            'publisher': row[6],
            'description': row[7],
            'total_copies': row[8],
            'available_copies': row[9],
            'location': row[10],
            'status': row[11],
            'created_at': row[12]
        })
    
    conn.close()
    return books

def add_book(title: str, author: str, isbn: str, category: str, publication_year: int, 
             publisher: str, description: str, total_copies: int, location: str) -> Tuple[bool, str]:
    """Add a new book to database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if ISBN already exists
        cursor.execute("SELECT id FROM library_books WHERE isbn = ?", (isbn,))
        if cursor.fetchone():
            conn.close()
            return False, "ISBN već postoji u bazi podataka"
        
        # Get next ID
        cursor.execute("SELECT MAX(id) FROM library_books")
        max_id = cursor.fetchone()[0]
        next_id = (max_id or 0) + 1
        
        cursor.execute('''
            INSERT INTO library_books 
            (id, title, author, isbn, category, publication_year, publisher, description, 
             total_copies, available_copies, location, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            next_id, title, author, isbn, category, publication_year, publisher, description,
            total_copies, total_copies, location, 'available', datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        return True, "Knjiga uspešno dodata"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Greška pri dodavanju knjige: {str(e)}"

def update_book(book_id: int, title: str, author: str, isbn: str, category: str, 
                publication_year: int, publisher: str, description: str, 
                total_copies: int, location: str) -> Tuple[bool, str]:
    """Update an existing book"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if ISBN exists for another book
        cursor.execute("SELECT id FROM library_books WHERE isbn = ? AND id != ?", (isbn, book_id))
        if cursor.fetchone():
            conn.close()
            return False, "ISBN već postoji za drugu knjigu"
        
        cursor.execute('''
            UPDATE library_books 
            SET title = ?, author = ?, isbn = ?, category = ?, publication_year = ?,
                publisher = ?, description = ?, total_copies = ?, location = ?, updated_at = ?
            WHERE id = ?
        ''', (title, author, isbn, category, publication_year, publisher, description,
              total_copies, location, datetime.now().isoformat(), book_id))
        
        if cursor.rowcount == 0:
            conn.close()
            return False, "Knjiga nije pronađena"
        
        conn.commit()
        conn.close()
        return True, "Knjiga uspešno ažurirana"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Greška pri ažuriranju knjige: {str(e)}"

def delete_book(book_id: int) -> Tuple[bool, str]:
    """Delete a book from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if book has active loans
        cursor.execute("SELECT COUNT(*) FROM library_loans WHERE book_id = ? AND status = 'active'", (book_id,))
        active_loans = cursor.fetchone()[0]
        
        if active_loans > 0:
            conn.close()
            return False, "Ne možete obrisati knjigu koja ima aktivne pozajmice"
        
        cursor.execute("DELETE FROM library_books WHERE id = ?", (book_id,))
        
        if cursor.rowcount == 0:
            conn.close()
            return False, "Knjiga nije pronađena"
        
        conn.commit()
        conn.close()
        return True, "Knjiga uspešno obrisana"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Greška pri brisanju knjige: {str(e)}"

# Member operations
def get_all_members() -> List[Dict]:
    """Get all members from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, first_name, last_name, email, phone, address, membership_number,
               membership_type, membership_status, membership_start_date, membership_end_date,
               max_loans, current_loans, created_at, updated_at
        FROM library_members
        ORDER BY last_name, first_name
    ''')
    
    members = []
    for row in cursor.fetchall():
        members.append({
            'id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'email': row[3],
            'phone': row[4],
            'address': row[5],
            'membership_number': row[6],
            'membership_type': row[7],
            'membership_status': row[8],
            'membership_start_date': row[9],
            'membership_end_date': row[10],
            'max_loans': row[11],
            'current_loans': row[12],
            'created_at': row[13],
            'updated_at': row[14]
        })
    
    conn.close()
    return members

def add_member(first_name: str, last_name: str, email: str, phone: str, address: str,
               membership_number: str, membership_type: str) -> Tuple[bool, str]:
    """Add a new member to database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if email or membership number already exists
        cursor.execute("SELECT id FROM library_members WHERE email = ? OR membership_number = ?", 
                      (email, membership_number))
        if cursor.fetchone():
            conn.close()
            return False, "Email ili broj članstva već postoji"
        
        # Get next ID
        cursor.execute("SELECT MAX(id) FROM library_members")
        max_id = cursor.fetchone()[0]
        next_id = (max_id or 0) + 1
        
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=365)  # 1 year membership
        
        cursor.execute('''
            INSERT INTO library_members 
            (id, first_name, last_name, email, phone, address, membership_number,
             membership_type, membership_status, membership_start_date, membership_end_date,
             max_loans, current_loans, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            next_id, first_name, last_name, email, phone, address, membership_number,
            membership_type, 'active', start_date.isoformat(), end_date.isoformat(),
            5, 0, datetime.now().isoformat(), datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        return True, "Član uspešno dodat"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Greška pri dodavanju člana: {str(e)}"

def update_member(member_id: int, first_name: str, last_name: str, phone: str, address: str,
                 membership_type: str, membership_status: str) -> Tuple[bool, str]:
    """Update an existing member"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE library_members 
            SET first_name = ?, last_name = ?, phone = ?, address = ?,
                membership_type = ?, membership_status = ?, updated_at = ?
            WHERE id = ?
        ''', (first_name, last_name, phone, address, membership_type, 
              membership_status, datetime.now().isoformat(), member_id))
        
        if cursor.rowcount == 0:
            conn.close()
            return False, "Član nije pronađen"
        
        conn.commit()
        conn.close()
        return True, "Član uspešno ažuriran"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Greška pri ažuriranju člana: {str(e)}"

def delete_member(member_id: int) -> Tuple[bool, str]:
    """Delete a member from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if member has active loans
        cursor.execute("SELECT COUNT(*) FROM library_loans WHERE member_id = ? AND status = 'active'", (member_id,))
        active_loans = cursor.fetchone()[0]
        
        if active_loans > 0:
            conn.close()
            return False, "Ne možete obrisati člana koji ima aktivne pozajmice"
        
        cursor.execute("DELETE FROM library_members WHERE id = ?", (member_id,))
        
        if cursor.rowcount == 0:
            conn.close()
            return False, "Član nije pronađen"
        
        conn.commit()
        conn.close()
        return True, "Član uspešno obrisan"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Greška pri brisanju člana: {str(e)}"

# Loan operations
def get_all_loans() -> List[Dict]:
    """Get all loans from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT l.id, l.book_id, b.title as book_title, l.member_id, 
               m.first_name || ' ' || m.last_name as member_name,
               l.loan_date, l.due_date, l.return_date, l.status
        FROM library_loans l
        JOIN library_books b ON l.book_id = b.id
        JOIN library_members m ON l.member_id = m.id
        ORDER BY l.loan_date DESC
    ''')
    
    loans = []
    for row in cursor.fetchall():
        loans.append({
            'id': row[0],
            'book_id': row[1],
            'book_title': row[2],
            'member_id': row[3],
            'member_name': row[4],
            'loan_date': row[5],
            'due_date': row[6],
            'return_date': row[7],
            'status': row[8]
        })
    
    conn.close()
    return loans

def create_loan(book_id: int, member_id: int) -> Tuple[bool, str]:
    """Create a new loan"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if book is available
        cursor.execute("SELECT available_copies FROM library_books WHERE id = ?", (book_id,))
        book_result = cursor.fetchone()
        if not book_result:
            conn.close()
            return False, "Knjiga nije pronađena"
        
        available_copies = book_result[0]
        if available_copies <= 0:
            conn.close()
            return False, "Knjiga nije dostupna za pozajmljivanje"
        
        # Check if member can borrow
        cursor.execute("SELECT current_loans, max_loans FROM library_members WHERE id = ?", (member_id,))
        member_result = cursor.fetchone()
        if not member_result:
            conn.close()
            return False, "Član nije pronađen"
        
        current_loans, max_loans = member_result
        if current_loans >= max_loans:
            conn.close()
            return False, "Član je dostigao maksimalan broj pozajmica"
        
        # Get next loan ID
        cursor.execute("SELECT MAX(id) FROM library_loans")
        max_id = cursor.fetchone()[0]
        next_id = (max_id or 0) + 1
        
        loan_date = datetime.now().date()
        due_date = loan_date + timedelta(days=14)  # 2 weeks loan period
        
        cursor.execute('''
            INSERT INTO library_loans 
            (id, book_id, member_id, loan_date, due_date, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (next_id, book_id, member_id, loan_date.isoformat(), due_date.isoformat(), 'active'))
        
        # Update book available copies
        cursor.execute('''
            UPDATE library_books 
            SET available_copies = available_copies - 1
            WHERE id = ?
        ''', (book_id,))
        
        # Update member current loans
        cursor.execute('''
            UPDATE library_members 
            SET current_loans = current_loans + 1
            WHERE id = ?
        ''', (member_id,))
        
        conn.commit()
        conn.close()
        return True, "Pozajmica uspešno kreirana"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Greška pri kreiranju pozajmice: {str(e)}"

def return_loan(loan_id: int) -> Tuple[bool, str]:
    """Return a loan"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get loan details
        cursor.execute('''
            SELECT book_id, member_id, status FROM library_loans WHERE id = ?
        ''', (loan_id,))
        loan_result = cursor.fetchone()
        
        if not loan_result:
            conn.close()
            return False, "Pozajmica nije pronađena"
        
        book_id, member_id, status = loan_result
        
        if status != 'active':
            conn.close()
            return False, "Pozajmica je već vraćena"
        
        # Update loan status
        cursor.execute('''
            UPDATE library_loans 
            SET status = 'returned', return_date = ?, updated_at = ?
            WHERE id = ?
        ''', (datetime.now().date().isoformat(), datetime.now().isoformat(), loan_id))
        
        # Update book available copies
        cursor.execute('''
            UPDATE library_books 
            SET available_copies = available_copies + 1
            WHERE id = ?
        ''', (book_id,))
        
        # Update member current loans
        cursor.execute('''
            UPDATE library_members 
            SET current_loans = current_loans - 1
            WHERE id = ?
        ''', (member_id,))
        
        conn.commit()
        conn.close()
        return True, "Pozajmica uspešno vraćena"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Greška pri vraćanju pozajmice: {str(e)}"

def update_loan(loan_id: int, due_date: str) -> Tuple[bool, str]:
    """Update a loan (mainly the due date)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if loan exists
        cursor.execute("SELECT id, status FROM library_loans WHERE id = ?", (loan_id,))
        loan_result = cursor.fetchone()
        
        if not loan_result:
            conn.close()
            return False, "Pozajmica nije pronađena"
        
        if loan_result[1] != 'active':
            conn.close()
            return False, "Ne možete ažurirati vraćenu pozajmicu"
        
        cursor.execute('''
            UPDATE library_loans 
            SET due_date = ?, updated_at = ?
            WHERE id = ?
        ''', (due_date, datetime.now().isoformat(), loan_id))
        
        conn.commit()
        conn.close()
        return True, "Pozajmica uspešno ažurirana"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Greška pri ažuriranju pozajmice: {str(e)}"

def delete_loan(loan_id: int) -> Tuple[bool, str]:
    """Delete a loan (only if not returned)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT book_id, member_id, status FROM library_loans WHERE id = ?
        ''', (loan_id,))
        loan_result = cursor.fetchone()
        if not loan_result:
            conn.close()
            return False, "Pozajmica nije pronađena"
        book_id, member_id, status = loan_result
        if status == 'active':
            cursor.execute('''
                UPDATE library_books
                SET available_copies = available_copies + 1
                WHERE id = ?
            ''', (book_id,))
            cursor.execute('''
                UPDATE library_members
                SET current_loans = current_loans - 1
                WHERE id = ?
            ''', (member_id,))
        cursor.execute("DELETE FROM library_loans WHERE id = ?", (loan_id,))
        conn.commit()
        conn.close()
        return True, "Pozajmica uspešno obrisana"
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Greška pri brisanju pozajmice: {str(e)}"

# Reservation operations
def create_reservation(book_id: int, member_id: int) -> Tuple[bool, str]:
    """Create a new reservation"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if book exists
        cursor.execute("SELECT title, available_copies FROM library_books WHERE id = ?", (book_id,))
        book_result = cursor.fetchone()
        if not book_result:
            conn.close()
            return False, "Knjiga nije pronađena"
        
        book_title, available_copies = book_result
        
        # Check if member exists
        cursor.execute("SELECT first_name, last_name FROM library_members WHERE id = ?", (member_id,))
        member_result = cursor.fetchone()
        if not member_result:
            conn.close()
            return False, "Član nije pronađen"
        
        # Check if book is already reserved by this member
        cursor.execute("""
            SELECT id FROM library_reservations 
            WHERE book_id = ? AND member_id = ? AND status = 'active'
        """, (book_id, member_id))
        if cursor.fetchone():
            conn.close()
            return False, "Već ste rezervisali ovu knjigu"
        
        # Get next reservation ID
        cursor.execute("SELECT MAX(id) FROM library_reservations")
        max_id = cursor.fetchone()[0]
        next_id = (max_id or 0) + 1
        
        # Create reservation (7 days expiry)
        reservation_date = datetime.now().date()
        expiry_date = reservation_date + timedelta(days=7)
        
        cursor.execute('''
            INSERT INTO library_reservations 
            (id, book_id, member_id, reservation_date, expiry_date, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            next_id, book_id, member_id, reservation_date.isoformat(), 
            expiry_date.isoformat(), 'active', datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        return True, f"Knjiga '{book_title}' je uspešno rezervisana"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Greška pri kreiranju rezervacije: {str(e)}"

def get_member_reservations(member_id: int) -> List[Dict]:
    """Get all reservations for a member"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT r.id, r.book_id, b.title, b.author, r.reservation_date, 
                   r.expiry_date, r.status, r.created_at
            FROM library_reservations r
            JOIN library_books b ON r.book_id = b.id
            WHERE r.member_id = ?
            ORDER BY r.created_at DESC
        ''', (member_id,))
        
        reservations = []
        for row in cursor.fetchall():
            reservations.append({
                'id': row[0],
                'book_id': row[1],
                'book_title': row[2],
                'book_author': row[3],
                'reservation_date': row[4],
                'expiry_date': row[5],
                'status': row[6],
                'created_at': row[7]
            })
        
        conn.close()
        return reservations
        
    except Exception as e:
        if conn:
            conn.close()
        return []

def cancel_reservation(reservation_id: int, member_id: int) -> Tuple[bool, str]:
    """Cancel a reservation"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if reservation exists and belongs to member
        cursor.execute("""
            SELECT id FROM library_reservations 
            WHERE id = ? AND member_id = ? AND status = 'active'
        """, (reservation_id, member_id))
        
        if not cursor.fetchone():
            conn.close()
            return False, "Rezervacija nije pronađena ili je već otkazana"
        
        cursor.execute("""
            UPDATE library_reservations 
            SET status = 'cancelled', updated_at = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), reservation_id))
        
        conn.commit()
        conn.close()
        return True, "Rezervacija je uspešno otkazana"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Greška pri otkazivanju rezervacije: {str(e)}"

# User authentication
def authenticate_user(email: str, password_hash: str) -> Optional[Dict]:
    """Authenticate a user"""
    print(f"🔍 LIBRARY_DB: authenticate_user called with email: {email}")
    print(f"🔐 LIBRARY_DB: Password hash: {password_hash[:20]}...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("🔍 LIBRARY_DB: Executing database query...")
    cursor.execute('''
        SELECT id, email, password_hash, user_type, member_id
        FROM library_users
        WHERE email = ? AND password_hash = ?
    ''', (email, password_hash))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        print("✅ LIBRARY_DB: User found in database!")
        print(f"📋 LIBRARY_DB: Raw user data: {user}")
        user_dict = {
            'id': user[0],
            'email': user[1],
            'password_hash': user[2],
            'user_type': user[3],
            'member_id': user[4]
        }
        print(f"🎯 LIBRARY_DB: Returning user dict: {user_dict}")
        return user_dict
    else:
        print("❌ LIBRARY_DB: No user found with these credentials")
        return None

def create_user(email: str, password_hash: str, user_type: str = 'member', member_id: int = None) -> Tuple[bool, str]:
    """Create a new user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute("SELECT id FROM library_users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return False, "Email već postoji"
        
        cursor.execute('''
            INSERT INTO library_users (email, password_hash, user_type, member_id)
            VALUES (?, ?, ?, ?)
        ''', (email, password_hash, user_type, member_id))
        
        conn.commit()
        conn.close()
        return True, "Korisnik uspešno kreiran"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Greška pri kreiranju korisnika: {str(e)}"

# Statistics
def get_library_statistics() -> Dict:
    """Get library statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total books
    cursor.execute("SELECT COUNT(*) FROM library_books")
    total_books = cursor.fetchone()[0]
    
    # Available books
    cursor.execute("SELECT SUM(available_copies) FROM library_books")
    available_books = cursor.fetchone()[0] or 0
    
    # Total members
    cursor.execute("SELECT COUNT(*) FROM library_members")
    total_members = cursor.fetchone()[0]
    
    # Active loans
    cursor.execute("SELECT COUNT(*) FROM library_loans WHERE status = 'active'")
    active_loans = cursor.fetchone()[0]
    
    # Overdue loans
    cursor.execute("SELECT COUNT(*) FROM library_loans WHERE status = 'active' AND due_date < ?", 
                  (datetime.now().date().isoformat(),))
    overdue_loans = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_books': total_books,
        'available_books': available_books,
        'total_members': total_members,
        'active_loans': active_loans,
        'overdue_loans': overdue_loans
    }

def get_member_loans(member_id: int) -> List[Dict]:
    """Get all loans for a member"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT l.id, l.book_id, b.title, b.author, l.loan_date, 
                   l.due_date, l.status, l.created_at
            FROM library_loans l
            JOIN library_books b ON l.book_id = b.id
            WHERE l.member_id = ?
            ORDER BY l.created_at DESC
        ''', (member_id,))
        
        loans = []
        for row in cursor.fetchall():
            loans.append({
                'id': row[0],
                'book_id': row[1],
                'book_title': row[2],
                'book_author': row[3],
                'loan_date': row[4],
                'due_date': row[5],
                'status': row[6],
                'created_at': row[7]
            })
        
        conn.close()
        return loans
        
    except Exception as e:
        if conn:
            conn.close()
        return []

def has_member_borrowed_book(member_id: int, book_id: int) -> bool:
    """Check if a member has already borrowed a specific book"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM library_loans 
            WHERE member_id = ? AND book_id = ? AND status = 'active'
        ''', (member_id, book_id))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
        
    except Exception as e:
        if conn:
            conn.close()
        return False

def has_member_reserved_book(member_id: int, book_id: int) -> bool:
    """Check if a member has already reserved a specific book"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM library_reservations 
            WHERE member_id = ? AND book_id = ? AND status = 'active'
        ''', (member_id, book_id))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
        
    except Exception as e:
        if conn:
            conn.close()
        return False

def get_member_statistics(member_id: int) -> Dict:
    """Get comprehensive statistics for a specific member"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get member details
        cursor.execute('''
            SELECT first_name, last_name, membership_type, membership_number, 
                   max_loans, current_loans, membership_status
            FROM library_members 
            WHERE id = ?
        ''', (member_id,))
        
        member_result = cursor.fetchone()
        if not member_result:
            conn.close()
            return {}
        
        first_name, last_name, membership_type, membership_number, max_loans, current_loans, membership_status = member_result
        
        # Get active loans count from loans table (most accurate)
        cursor.execute('''
            SELECT COUNT(*) FROM library_loans 
            WHERE member_id = ? AND status = 'active'
        ''', (member_id,))
        active_loans = cursor.fetchone()[0]
        
        # Get active reservations count
        cursor.execute('''
            SELECT COUNT(*) FROM library_reservations 
            WHERE member_id = ? AND status = 'active'
        ''', (member_id,))
        active_reservations = cursor.fetchone()[0]
        
        # Get overdue loans count
        from datetime import datetime
        today = datetime.now().date().isoformat()
        cursor.execute('''
            SELECT COUNT(*) FROM library_loans 
            WHERE member_id = ? AND status = 'active' AND due_date < ?
        ''', (member_id, today))
        overdue_loans = cursor.fetchone()[0]
        
        # Get total books borrowed (all time)
        cursor.execute('''
            SELECT COUNT(*) FROM library_loans 
            WHERE member_id = ?
        ''', (member_id,))
        total_loans = cursor.fetchone()[0]
        
        # Get total available books in library
        cursor.execute('''
            SELECT SUM(available_copies) FROM library_books
        ''', )
        total_available_books = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'first_name': first_name,
            'last_name': last_name,
            'membership_type': membership_type,
            'membership_number': membership_number,
            'membership_status': membership_status,
            'max_loans': max_loans,
            'current_loans': current_loans,
            'active_loans': active_loans,  # Use this for display (from loans table)
            'active_reservations': active_reservations,
            'overdue_loans': overdue_loans,
            'total_loans': total_loans,
            'total_available_books': total_available_books
        }
        
    except Exception as e:
        if conn:
            conn.close()
        print(f"Error getting member statistics: {e}")
        return {}

def fix_member_loan_counts() -> bool:
    """Fix current_loans field in library_members table based on actual active loans"""
    try:
        print("🔧 FIXING: Starting member loan count correction...")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all members
        cursor.execute('SELECT id, first_name, last_name, current_loans FROM library_members')
        members = cursor.fetchall()
        
        fixed_count = 0
        
        for member_id, first_name, last_name, current_loans in members:
            # Count actual active loans for this member
            cursor.execute('''
                SELECT COUNT(*) FROM library_loans 
                WHERE member_id = ? AND status = 'active'
            ''', (member_id,))
            actual_active_loans = cursor.fetchone()[0]
            
            if current_loans != actual_active_loans:
                print(f"🔧 FIXING: Member {first_name} {last_name} (ID: {member_id})")
                print(f"   - Current field: {current_loans}, Actual loans: {actual_active_loans}")
                
                # Update the current_loans field
                cursor.execute('''
                    UPDATE library_members 
                    SET current_loans = ? 
                    WHERE id = ?
                ''', (actual_active_loans, member_id))
                
                fixed_count += 1
                print(f"   ✅ Fixed: Updated to {actual_active_loans}")
        
        if fixed_count > 0:
            conn.commit()
            print(f"🎉 FIXING: Fixed {fixed_count} member(s) loan counts")
        else:
            print("✅ FIXING: All member loan counts are already correct")
        
        conn.close()
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        print(f"💥 FIXING: Error fixing loan counts: {e}")
        return False
