from utils.global_state import global_state
from models.book import Book
from models.loan import Loan
from models.reservation import Reservation
from datetime import datetime, timedelta

def search_books(query: str = "", category: str = "", availability: str = "") -> list[Book]:
    """
    Search books based on query, category, and availability
    """
    books = global_state.get("books", [])
    
    # Mock books if none exist
    if not books:
        books = [
            Book(
                id=1,
                title="Ana Karenjina",
                author="Lav Tolstoj",
                isbn="978-86-521-1234-5",
                category="roman",
                publication_year=1877,
                publisher="Laguna",
                description="Klasičan ruski roman o ljubavi i društvenim konvencijama",
                total_copies=3,
                available_copies=1,
                location="Polica A1",
                status="available"
            ),
            Book(
                id=2,
                title="Rat i mir",
                author="Lav Tolstoj",
                isbn="978-86-521-2345-6",
                category="roman",
                publication_year=1869,
                publisher="Laguna",
                description="Ep o ruskom društvu tokom Napoleonovih ratova",
                total_copies=2,
                available_copies=0,
                location="Polica A1",
                status="unavailable"
            ),
            Book(
                id=3,
                title="Krimski sonet",
                author="Ivo Andrić",
                isbn="978-86-521-3456-7",
                category="poezija",
                publication_year=1959,
                publisher="Prosveta",
                description="Zbirka pesama inspirisana istorijom",
                total_copies=5,
                available_copies=3,
                location="Polica B2",
                status="available"
            ),
            Book(
                id=4,
                title="Na Drini ćuprija",
                author="Ivo Andrić",
                isbn="978-86-521-4567-8",
                category="roman",
                publication_year=1945,
                publisher="Prosveta",
                description="Roman o istoriji Bosne kroz most",
                total_copies=4,
                available_copies=2,
                location="Polica B2",
                status="available"
            ),
            Book(
                id=5,
                title="Gorski vijenac",
                author="Petar II Petrović Njegoš",
                isbn="978-86-521-5678-9",
                category="poezija",
                publication_year=1847,
                publisher="Prosveta",
                description="Ep o borbi za slobodu Crne Gore",
                total_copies=3,
                available_copies=1,
                location="Polica C3",
                status="available"
            )
        ]
        global_state.set("books", books)
    
    filtered_books = books
    
    # Apply search query
    if query:
        query_lower = query.lower()
        filtered_books = [
            book for book in filtered_books
            if query_lower in book.title.lower() or
               query_lower in book.author.lower() or
               query_lower in book.isbn.lower() or
               query_lower in book.description.lower()
        ]
    
    # Apply category filter
    if category and category != "all":
        filtered_books = [
            book for book in filtered_books
            if book.category == category
        ]
    
    # Apply availability filter
    if availability and availability != "all":
        if availability == "available":
            filtered_books = [
                book for book in filtered_books
                if book.available_copies > 0
            ]
        elif availability == "unavailable":
            filtered_books = [
                book for book in filtered_books
                if book.available_copies == 0
            ]
    
    return filtered_books

def borrow_book(book_id: int, member_id: int) -> tuple[bool, str]:
    """
    Borrow a book for a member
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
            return False, "Dostigli ste maksimalan broj pozajmica"
        
        if member.membership_status != "active":
            return False, "Vaše članstvo nije aktivno"
        
        # Create loan
        loans = global_state.get("loans", [])
        new_loan = Loan(
            id=len(loans) + 1,
            book_id=book_id,
            member_id=member_id,
            loan_date=datetime.now(),
            due_date=datetime.now() + timedelta(days=14),
            status="active",
            created_at=datetime.now()
        )
        
        loans.append(new_loan)
        global_state.set("loans", loans)
        
        # Update book and member
        book.available_copies -= 1
        member.current_loans += 1
        
        return True, f"Uspešno pozajmljena knjiga '{book.title}'. Rok vraćanja: {new_loan.due_date.strftime('%d.%m.%Y')}"
        
    except Exception as e:
        return False, f"Greška prilikom pozajmljivanja: {str(e)}"

def reserve_book(book_id: int, member_id: int) -> tuple[bool, str]:
    """
    Reserve a book for a member
    Returns: (success: bool, message: str)
    """
    try:
        books = global_state.get("books", [])
        members = global_state.get("members", [])
        reservations = global_state.get("reservations", [])
        
        book = next((b for b in books if b.id == book_id), None)
        member = next((m for m in members if m.id == member_id), None)
        
        if not book:
            return False, "Knjiga nije pronađena"
        
        if not member:
            return False, "Član nije pronađen"
        
        if member.membership_status != "active":
            return False, "Vaše članstvo nije aktivno"
        
        # Check if already reserved by this member
        existing_reservation = next(
            (r for r in reservations 
             if r.book_id == book_id and r.member_id == member_id and r.status == "active"),
            None
        )
        
        if existing_reservation:
            return False, "Već imate aktivnu rezervaciju za ovu knjigu"
        
        # Create reservation
        new_reservation = Reservation(
            id=len(reservations) + 1,
            book_id=book_id,
            member_id=member_id,
            reservation_date=datetime.now(),
            expiry_date=datetime.now() + timedelta(days=7),
            status="active",
            priority=1,
            created_at=datetime.now()
        )
        
        reservations.append(new_reservation)
        global_state.set("reservations", reservations)
        
        return True, f"Uspešno rezervisana knjiga '{book.title}'. Rezervacija važi do: {new_reservation.expiry_date.strftime('%d.%m.%Y')}"
        
    except Exception as e:
        return False, f"Greška prilikom rezervacije: {str(e)}"

def get_member_loans(member_id: int) -> list[Loan]:
    """
    Get all loans for a specific member
    """
    loans = global_state.get("loans", [])
    return [loan for loan in loans if loan.member_id == member_id]

def get_member_reservations(member_id: int) -> list[Reservation]:
    """
    Get all reservations for a specific member
    """
    reservations = global_state.get("reservations", [])
    return [res for res in reservations if res.member_id == member_id]

def get_book_categories() -> list[str]:
    """
    Get all available book categories
    """
    books = global_state.get("books", [])
    categories = list(set(book.category for book in books))
    return sorted(categories)


