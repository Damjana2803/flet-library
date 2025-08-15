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
        
        books = global_state.get("books", [])
        
        # Check if ISBN already exists
        if any(book.isbn == isbn for book in books):
            return False, "Knjiga sa ovim ISBN-om već postoji"
        
        new_book = Book(
            id=len(books) + 1,
            title=title,
            author=author,
            isbn=isbn,
            category=category,
            publication_year=publication_year,
            publisher=publisher,
            description=description,
            total_copies=total_copies,
            available_copies=total_copies,
            location=location,
            status="available",
            created_at=datetime.now()
        )
        
        books.append(new_book)
        global_state.set("books", books)
        
        return True, f"Knjiga '{title}' je uspešno dodata"
        
    except Exception as e:
        return False, f"Greška prilikom dodavanja knjige: {str(e)}"

def update_book(book_id: int, title: str, author: str, isbn: str, category: str, 
                publication_year: int, publisher: str, description: str, 
                total_copies: int, location: str) -> tuple[bool, str]:
    """
    Update an existing book
    Returns: (success: bool, message: str)
    """
    try:
        books = global_state.get("books", [])
        book = next((b for b in books if b.id == book_id), None)
        
        if not book:
            return False, "Knjiga nije pronađena"
        
        if not all([title, author, isbn, category, publication_year, publisher, total_copies, location]):
            return False, "Sva obavezna polja moraju biti popunjena"
        
        if publication_year < 1800 or publication_year > datetime.now().year:
            return False, "Nevažeća godina izdanja"
        
        if total_copies < (book.total_copies - book.available_copies):
            return False, "Broj primeraka ne može biti manji od pozajmljenih"
        
        # Check if ISBN already exists (excluding current book)
        if any(b.isbn == isbn and b.id != book_id for b in books):
            return False, "Knjiga sa ovim ISBN-om već postoji"
        
        # Update book
        book.title = title
        book.author = author
        book.isbn = isbn
        book.category = category
        book.publication_year = publication_year
        book.publisher = publisher
        book.description = description
        book.total_copies = total_copies
        book.available_copies = total_copies - (book.total_copies - book.available_copies)
        book.location = location
        book.updated_at = datetime.now()
        
        return True, f"Knjiga '{title}' je uspešno ažurirana"
        
    except Exception as e:
        return False, f"Greška prilikom ažuriranja knjige: {str(e)}"

def delete_book(book_id: int) -> tuple[bool, str]:
    """
    Delete a book from the library
    Returns: (success: bool, message: str)
    """
    try:
        books = global_state.get("books", [])
        book = next((b for b in books if b.id == book_id), None)
        
        if not book:
            return False, "Knjiga nije pronađena"
        
        # Check if book is currently borrowed
        loans = global_state.get("loans", [])
        active_loans = [l for l in loans if l.book_id == book_id and l.status == "active"]
        
        if active_loans:
            return False, "Knjiga ne može biti obrisana jer je trenutno pozajmljena"
        
        # Check if book has active reservations
        reservations = global_state.get("reservations", [])
        active_reservations = [r for r in reservations if r.book_id == book_id and r.status == "active"]
        
        if active_reservations:
            return False, "Knjiga ne može biti obrisana jer ima aktivne rezervacije"
        
        books.remove(book)
        global_state.set("books", books)
        
        return True, f"Knjiga '{book.title}' je uspešno obrisana"
        
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
        
        members = global_state.get("members", [])
        
        # Check if email already exists
        if any(member.email == email for member in members):
            return False, "Član sa ovom e-adresom već postoji"
        
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
            created_at=datetime.now()
        )
        
        members.append(new_member)
        global_state.set("members", members)
        
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
        members = global_state.get("members", [])
        member = next((m for m in members if m.id == member_id), None)
        
        if not member:
            return False, "Član nije pronađen"
        
        if not all([first_name, last_name, email, phone, address, membership_type, membership_status]):
            return False, "Sva obavezna polja moraju biti popunjena"
        
        # Check if email already exists (excluding current member)
        if any(m.email == email and m.id != member_id for m in members):
            return False, "Član sa ovom e-adresom već postoji"
        
        # Update member
        member.first_name = first_name
        member.last_name = last_name
        member.email = email
        member.phone = phone
        member.address = address
        member.membership_type = membership_type
        member.membership_status = membership_status
        member.updated_at = datetime.now()
        
        return True, f"Član '{member.full_name}' je uspešno ažuriran"
        
    except Exception as e:
        return False, f"Greška prilikom ažuriranja člana: {str(e)}"

def delete_member(member_id: int) -> tuple[bool, str]:
    """
    Delete a member from the library
    Returns: (success: bool, message: str)
    """
    try:
        members = global_state.get("members", [])
        member = next((m for m in members if m.id == member_id), None)
        
        if not member:
            return False, "Član nije pronađen"
        
        # Check if member has active loans
        loans = global_state.get("loans", [])
        active_loans = [l for l in loans if l.member_id == member_id and l.status == "active"]
        
        if active_loans:
            return False, "Član ne može biti obrisan jer ima aktivne pozajmice"
        
        # Check if member has active reservations
        reservations = global_state.get("reservations", [])
        active_reservations = [r for r in reservations if r.member_id == member_id and r.status == "active"]
        
        if active_reservations:
            return False, "Član ne može biti obrisan jer ima aktivne rezervacije"
        
        members.remove(member)
        global_state.set("members", members)
        
        return True, f"Član '{member.full_name}' je uspešno obrisan"
        
    except Exception as e:
        return False, f"Greška prilikom brisanja člana: {str(e)}"

def create_loan(book_id: int, member_id: int, duration_days: int = 14) -> tuple[bool, str]:
    """
    Create a new loan
    Returns: (success: bool, message: str)
    """
    try:
        books = global_state.get("books", [])
        members = global_state.get("members", [])
        
        book = next((b for b in books if b.id == book_id), None)
        member = next((m for m in members if m.id == member_id), None)
        
        if not book:
            return False, "Knjiga nije pronađena"
        
        if not member:
            return False, "Član nije pronađen"
        
        if book.available_copies <= 0:
            return False, "Knjiga nije dostupna za pozajmljivanje"
        
        if member.current_loans >= member.max_loans:
            return False, "Član je dostigao maksimalan broj pozajmica"
        
        if member.membership_status != "active":
            return False, "Članstvo nije aktivno"
        
        # Create loan
        loans = global_state.get("loans", [])
        new_loan = Loan(
            id=len(loans) + 1,
            book_id=book_id,
            member_id=member_id,
            loan_date=datetime.now(),
            due_date=datetime.now() + timedelta(days=duration_days),
            status="active",
            created_at=datetime.now()
        )
        
        loans.append(new_loan)
        global_state.set("loans", loans)
        
        # Update book and member
        book.available_copies -= 1
        member.current_loans += 1
        
        return True, f"Pozajmica je uspešno kreirana. Rok vraćanja: {new_loan.due_date.strftime('%d.%m.%Y')}"
        
    except Exception as e:
        return False, f"Greška prilikom kreiranja pozajmice: {str(e)}"

def return_loan(loan_id: int) -> tuple[bool, str]:
    """
    Return a loaned book
    Returns: (success: bool, message: str)
    """
    try:
        loans = global_state.get("loans", [])
        loan = next((l for l in loans if l.id == loan_id), None)
        
        if not loan:
            return False, "Pozajmica nije pronađena"
        
        if loan.status != "active":
            return False, "Pozajmica nije aktivna"
        
        books = global_state.get("books", [])
        members = global_state.get("members", [])
        
        book = next((b for b in books if b.id == loan.book_id), None)
        member = next((m for m in members if m.id == loan.member_id), None)
        
        # Update loan
        loan.return_date = datetime.now()
        loan.status = "returned"
        loan.updated_at = datetime.now()
        
        # Update book and member
        if book:
            book.available_copies += 1
        if member:
            member.current_loans -= 1
        
        return True, "Knjiga je uspešno vraćena"
        
    except Exception as e:
        return False, f"Greška prilikom vraćanja knjige: {str(e)}"

def get_statistics() -> dict:
    """
    Get library statistics
    Returns: dict with various statistics
    """
    try:
        books = global_state.get("books", [])
        members = global_state.get("members", [])
        loans = global_state.get("loans", [])
        reservations = global_state.get("reservations", [])
        
        # Basic counts
        total_books = len(books)
        total_members = len(members)
        total_loans = len(loans)
        total_reservations = len(reservations)
        
        # Available books
        available_books = sum(book.available_copies for book in books)
        borrowed_books = sum(book.total_copies - book.available_copies for book in books)
        
        # Active members
        active_members = len([m for m in members if m.membership_status == "active"])
        suspended_members = len([m for m in members if m.membership_status == "suspended"])
        expired_members = len([m for m in members if m.membership_status == "expired"])
        
        # Active loans
        active_loans = len([l for l in loans if l.status == "active"])

        returned_loans = len([l for l in loans if l.status == "returned"])
        
        # Active reservations
        active_reservations = len([r for r in reservations if r.status == "active"])
        fulfilled_reservations = len([r for r in reservations if r.status == "fulfilled"])
        expired_reservations = len([r for r in reservations if r.status == "expired"])
        
        # Popular books (by loan count)
        book_loan_counts = {}
        for loan in loans:
            book_loan_counts[loan.book_id] = book_loan_counts.get(loan.book_id, 0) + 1
        
        popular_books = []
        for book_id, count in sorted(book_loan_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            book = next((b for b in books if b.id == book_id), None)
            if book:
                popular_books.append({"title": book.title, "author": book.author, "loans": count})
        
        # Membership distribution
        membership_distribution = {}
        for member in members:
            membership_distribution[member.membership_type] = membership_distribution.get(member.membership_type, 0) + 1
        
        return {
            "total_books": total_books,
            "available_books": available_books,
            "borrowed_books": borrowed_books,
            "total_members": total_members,
            "active_members": active_members,
            "suspended_members": suspended_members,
            "expired_members": expired_members,
            "total_loans": total_loans,
            "active_loans": active_loans,

            "returned_loans": returned_loans,
            "total_reservations": total_reservations,
            "active_reservations": active_reservations,
            "fulfilled_reservations": fulfilled_reservations,
            "expired_reservations": expired_reservations,
            "popular_books": popular_books,
            "membership_distribution": membership_distribution
        }
        
    except Exception as e:
        return {"error": f"Greška prilikom generisanja statistike: {str(e)}"}