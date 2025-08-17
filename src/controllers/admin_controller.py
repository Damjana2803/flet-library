from models.user import User
from models.faculty import Faculty
from utils.global_state import global_state
from models.book import Book
from models.member import Member
from models.loan import Loan
from models.reservation import Reservation
from datetime import datetime, timedelta

async def get_all_users():
	user_model = User()

	users = user_model.get_all_users()

	return users

async def edit_user(user_id: int, name: str, faculty: str):
	user_model = User()
	faculty_model = Faculty()
	
	errors = []

	faculty_res = faculty_model.find_if_faculty_exists(faculty)

	if faculty is None:
		errors.append({ 'field': 'faculty', 'message': 'Fakultet je obavezno polje' })

	if len(errors):
		return {
			'success': False,
			'errors': errors
		}
	
	edited_successfully = user_model.edit_user(user_id, name, faculty_res)

	if not edited_successfully:
		errors.append({ 'field': 'name', 'message': 'Neočekivana greška' })

	return {
		'success': edited_successfully,
		'errors': errors
	}
	
async def delete_user(user_id: int):
	user_model = User()
	errors = []

	deleted_successfully = user_model.delete_user(user_id)

	return deleted_successfully



def add_book(title: str, author: str, isbn: str, category: str, publication_year: int, 
             publisher: str, description: str, total_copies: int, location: str) -> tuple[bool, str]:
    """
    Add a new book to the library
    Returns: (success: bool, message: str)
    """
    try:
        if not all([title, author, isbn, category, publication_year, publisher, total_copies, location]):
            return False, "Sva obavezna polja moraju biti popunjena"
        
        if publication_year < 1800 or publication_year > datetime.now().year:
            return False, "Nevažeća godina izdanja"
        
        if total_copies <= 0:
            return False, "Broj primeraka mora biti veći od 0"
        
        books = global_state.books
        
        # Check if ISBN already exists
        for book in books:
            if book.get('isbn', '') == isbn:
                return False, "Knjiga sa ovim ISBN-om već postoji"
        
        new_book = {
            'id': len(books) + 1,
            'title': title,
            'author': author,
            'isbn': isbn,
            'category': category,
            'publication_year': publication_year,
            'publisher': publisher,
            'description': description,
            'total_copies': total_copies,
            'available_copies': total_copies,
            'location': location,
            'status': "available",
            'created_at': datetime.now().isoformat()
        }
        
        books.append(new_book)
        global_state.books = books  # Set directly on the object
        global_state.save_data_to_file()  # Explicitly save to file
        
        return True, f"Knjiga '{title}' je uspešno dodata"
        
    except Exception as e:
        return False, f"Greška prilikom dodavanja knjige: {str(e)}"

def get_all_books():
    """
    Get all books from the library
    Returns: list of books
    """
    try:
        return global_state.books  # Direct access to books list
    except Exception as e:
        print(f"Greška pri učitavanju knjiga: {str(e)}")
        return []

def update_book(book_id: int, title: str, author: str, isbn: str, category: str, 
                publication_year: int, publisher: str, description: str, 
                total_copies: int, location: str) -> tuple[bool, str]:
    """
    Update an existing book
    Returns: (success: bool, message: str)
    """
    try:
        books = global_state.books
        book = None
        for b in books:
            if b.get('id') == book_id:
                book = b
                break
        
        if not book:
            return False, "Knjiga nije pronađena"
        
        if not all([title, author, isbn, category, publication_year, publisher, total_copies, location]):
            return False, "Sva obavezna polja moraju biti popunjena"
        
        if publication_year < 1800 or publication_year > datetime.now().year:
            return False, "Nevažeća godina izdanja"
        
        # Get book properties safely
        book_total_copies = book.get('total_copies', 0)
        book_available_copies = book.get('available_copies', 0)
        
        if total_copies < (book_total_copies - book_available_copies):
            return False, "Broj primeraka ne može biti manji od pozajmljenih"
        
        # Check if ISBN already exists (excluding current book)
        for b in books:
            b_id = b.get('id')
            b_isbn = b.get('isbn', '')
            if b_isbn == isbn and b_id != book_id:
                return False, "Knjiga sa ovim ISBN-om već postoji"
        
        # Update book
        book['title'] = title
        book['author'] = author
        book['isbn'] = isbn
        book['category'] = category
        book['publication_year'] = publication_year
        book['publisher'] = publisher
        book['description'] = description
        book['total_copies'] = total_copies
        book['available_copies'] = total_copies - (book_total_copies - book_available_copies)
        book['location'] = location
        book['updated_at'] = datetime.now().isoformat()
        
        # Save changes to global state
        global_state.books = books  # Set directly on the object
        global_state.save_data_to_file()  # Explicitly save to file
        
        return True, f"Knjiga '{title}' je uspešno ažurirana"
        
    except Exception as e:
        return False, f"Greška prilikom ažuriranja knjige: {str(e)}"

def delete_book(book_id: int) -> tuple[bool, str]:
    """
    Delete a book from the library
    Returns: (success: bool, message: str)
    """
    try:
        books = global_state.books
        book = None
        for b in books:
            if b.get('id') == book_id:
                book = b
                break
        
        if not book:
            return False, "Knjiga nije pronađena"
        
        # Check if book is currently borrowed
        loans = global_state.loans
        active_loans = [l for l in loans if l.book_id == book_id and l.status == "active"]
        
        if active_loans:
            return False, "Knjiga ne može biti obrisana jer je trenutno pozajmljena"
        
        # Check if book has active reservations
        reservations = global_state.reservations
        active_reservations = [r for r in reservations if r.book_id == book_id and r.status == "active"]
        
        if active_reservations:
            return False, "Knjiga ne može biti obrisana jer ima aktivne rezervacije"
        
        books.remove(book)
        global_state.books = books  # Set directly on the object
        global_state.save_data_to_file()  # Explicitly save to file
        
        book_title = book.get('title', 'Nepoznata knjiga')
        return True, f"Knjiga '{book_title}' je uspešno obrisana"
        
    except Exception as e:
        return False, f"Greška prilikom brisanja knjige: {str(e)}"

def add_member(first_name: str, last_name: str, email: str, phone: str, address: str, 
               membership_type: str) -> tuple[bool, str]:
    """
    Add a new member to the library
    Returns: (success: bool, message: str)
    """
    try:
        if not all([first_name, last_name, email, phone, address, membership_type]):
            return False, "Sva obavezna polja moraju biti popunjena"
        
        members = global_state.members
        
        # Check if email already exists
        if any(member.email == email for member in members):
            return False, "Član sa ovom e-adresom već postoji"
        
        # Set max loans based on membership type
        max_loans = 5  # Default for regular
        if membership_type == 'student':
            max_loans = 3
        elif membership_type == 'senior':
            max_loans = 7
        
        new_member = Member(
            id=len(members) + 1,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            membership_number=f"MEM{len(members) + 1:03d}",
            membership_type=membership_type,
            membership_status="active",
            membership_start_date=datetime.now(),
            membership_end_date=datetime.now().replace(year=datetime.now().year + 1),
            max_loans=max_loans,
            created_at=datetime.now()
        )
        
        members.append(new_member)
        global_state.members = members
        global_state.save_data_to_file()
        
        return True, f"Član '{new_member.full_name}' je uspešno dodat"
        
    except Exception as e:
        return False, f"Greška prilikom dodavanja člana: {str(e)}"

def update_member(member_id: int, first_name: str, last_name: str, email: str, phone: str, 
                 address: str, membership_type: str, membership_status: str) -> tuple[bool, str]:
    """
    Update an existing member
    Returns: (success: bool, message: str)
    """
    try:
        members = global_state.members
        member = next((m for m in members if m.id == member_id), None)
        
        if not member:
            return False, "Član nije pronađen"
        
        if not all([first_name, last_name, email, phone, address, membership_type, membership_status]):
            return False, "Sva obavezna polja moraju biti popunjena"
        
        # Check if email already exists (excluding current member)
        if any(m.email == email and m.id != member_id for m in members):
            return False, "Član sa ovom e-adresom već postoji"
        
        # Set max loans based on membership type
        max_loans = 5  # Default for regular
        if membership_type == 'student':
            max_loans = 3
        elif membership_type == 'senior':
            max_loans = 7
        
        # Update member
        member.first_name = first_name
        member.last_name = last_name
        member.email = email
        member.phone = phone
        member.address = address
        member.membership_type = membership_type
        member.membership_status = membership_status
        member.max_loans = max_loans
        member.updated_at = datetime.now()
        
        global_state.members = members
        global_state.save_data_to_file()
        
        return True, f"Član '{member.full_name}' je uspešno ažuriran"
        
    except Exception as e:
        return False, f"Greška prilikom ažuriranja člana: {str(e)}"

def delete_member(member_id: int) -> tuple[bool, str]:
    """
    Delete a member from the library
    Returns: (success: bool, message: str)
    """
    try:
        members = global_state.members
        member = next((m for m in members if m.id == member_id), None)
        
        if not member:
            return False, "Član nije pronađen"
        
        # Check if member has active loans
        loans = global_state.loans
        active_loans = [l for l in loans if l.member_id == member_id and l.status == "active"]
        
        if active_loans:
            return False, "Član ne može biti obrisan jer ima aktivne pozajmice"
        
        members.remove(member)
        global_state.members = members
        global_state.save_data_to_file()
        
        return True, f"Član '{member.full_name}' je uspešno obrisan"
        
    except Exception as e:
        return False, f"Greška prilikom brisanja člana: {str(e)}"

def get_all_members():
    """
    Get all members from the library
    Returns: list of members
    """
    try:
        return global_state.members
    except Exception as e:
        print(f"Greška pri učitavanju članova: {str(e)}")
        return []

def add_loan(book_id: int, member_id: int, loan_date: datetime = None, 
             due_date: datetime = None) -> tuple[bool, str]:
    """
    Add a new loan to the library
    Returns: (success: bool, message: str)
    """
    try:
        books = global_state.books
        members = global_state.members
        
        # Find book and member
        book = next((b for b in books if b.get('id') == book_id), None)
        member = next((m for m in members if m.id == member_id), None)
        
        if not book:
            return False, "Knjiga nije pronađena"
        
        if not member:
            return False, "Član nije pronađen"
        
        # Check if book is available
        if book.get('available_copies', 0) <= 0:
            return False, "Knjiga nije dostupna za pozajmljivanje"
        
        # Check if member has reached loan limit
        loans = global_state.loans
        active_loans = [l for l in loans if l.member_id == member_id and l.status == "active"]
        
        # Get member's max loans based on membership type
        member = next((m for m in global_state.members if m.get('id') == member_id), None)
        max_loans = 5  # Default
        if member:
            membership_type = member.get('membership_type', 'regular')
            if membership_type == 'student':
                max_loans = 3
            elif membership_type == 'senior':
                max_loans = 7
            else:  # regular
                max_loans = 5
        
        if len(active_loans) >= max_loans:
            return False, f"Član je dostigao maksimalan broj pozajmica ({max_loans})"
        
        # Set default dates if not provided
        if loan_date is None:
            loan_date = datetime.now()
        if due_date is None:
            due_date = loan_date + timedelta(days=14)  # 2 weeks default
        
        new_loan = Loan(
            id=len(loans) + 1,
            book_id=book_id,
            member_id=member_id,
            loan_date=loan_date,
            due_date=due_date,
            status="active",
            created_at=datetime.now()
        )
        
        # Update book availability
        book['available_copies'] = book.get('available_copies', 0) - 1
        
        loans.append(new_loan)
        global_state.loans = loans
        global_state.books = books
        global_state.save_data_to_file()
        
        return True, f"Pozajmica je uspešno kreirana"
        
    except Exception as e:
        return False, f"Greška prilikom kreiranja pozajmice: {str(e)}"

def return_book(loan_id: int) -> tuple[bool, str]:
    """
    Return a book (mark loan as returned)
    Returns: (success: bool, message: str)
    """
    try:
        loans = global_state.loans
        loan = next((l for l in loans if l.id == loan_id), None)
        
        if not loan:
            return False, "Pozajmica nije pronađena"
        
        if loan.status != "active":
            return False, "Pozajmica je već vraćena"
        
        # Update loan status
        loan.status = "returned"
        loan.return_date = datetime.now()
        
        # Update book availability
        books = global_state.books
        book = next((b for b in books if b.get('id') == loan.book_id), None)
        
        if book:
            book['available_copies'] = book.get('available_copies', 0) + 1
            global_state.books = books
        
        global_state.loans = loans
        global_state.save_data_to_file()
        
        return True, "Knjiga je uspešno vraćena"
        
    except Exception as e:
        return False, f"Greška prilikom vraćanja knjige: {str(e)}"

def get_all_loans():
    """
    Get all loans from the library
    Returns: list of loans
    """
    try:
        return global_state.loans
    except Exception as e:
        print(f"Greška pri učitavanju pozajmica: {str(e)}")
        return []

def get_library_statistics():
    """
    Get library statistics
    Returns: dictionary with statistics
    """
    try:
        books = global_state.books
        members = global_state.members
        loans = global_state.loans
        
        total_books = len(books)
        total_members = len(members)
        total_loans = len(loans)
        active_loans = len([l for l in loans if l.status == "active"])
        
        available_books = sum(book.get('available_copies', 0) for book in books)
        borrowed_books = sum(book.get('total_copies', 0) - book.get('available_copies', 0) for book in books)
        
        # Most popular books (by number of loans)
        book_loan_counts = {}
        for loan in loans:
            book_id = loan.book_id
            book_loan_counts[book_id] = book_loan_counts.get(book_id, 0) + 1
        
        most_popular_books = []
        for book_id, count in sorted(book_loan_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            book = next((b for b in books if b.get('id') == book_id), None)
            if book:
                most_popular_books.append({
                    'title': book.get('title', 'Nepoznata knjiga'),
                    'loans': count
                })
        
        return {
            'total_books': total_books,
            'total_members': total_members,
            'total_loans': total_loans,
            'active_loans': active_loans,
            'available_books': available_books,
            'borrowed_books': borrowed_books,
            'most_popular_books': most_popular_books
        }
        
    except Exception as e:
        print(f"Greška pri učitavanju statistike: {str(e)}")
        return {}