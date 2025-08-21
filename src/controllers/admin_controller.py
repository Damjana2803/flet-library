from models.user import User
from models.faculty import Faculty
from utils.global_state import global_state
from models.book import Book
from models.member import Member
from models.loan import Loan
from models.reservation import Reservation
from datetime import datetime, timedelta
from utils.library_db import (
    get_all_books as db_get_all_books,
    add_book as db_add_book,
    update_book as db_update_book,
    delete_book as db_delete_book,
    get_all_members as db_get_all_members,
    add_member as db_add_member,
    update_member as db_update_member,
    delete_member as db_delete_member,
    get_all_loans as db_get_all_loans,
    create_loan as db_create_loan,
    return_loan as db_return_loan,
    update_loan as db_update_loan,
    delete_loan as db_delete_loan,
    get_library_statistics as db_get_library_statistics
)

async def get_all_users():
    # This function is for legacy Athena system
    pass

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



def add_book(title, author, isbn, category, publication_year, publisher, description, total_copies, location):
    """Add a new book to the library"""
    return db_add_book(title, author, isbn, category, publication_year, publisher, description, total_copies, location)

def get_all_books():
    """Get all books from the library"""
    return db_get_all_books()

def update_book(book_id, title, author, isbn, category, publication_year, publisher, description, total_copies, location):
    """Update an existing book"""
    return db_update_book(book_id, title, author, isbn, category, publication_year, publisher, description, total_copies, location)

def delete_book(book_id):
    """Delete a book from the library"""
    return db_delete_book(book_id)

def add_member(first_name, last_name, email, phone, address, membership_number, membership_type):
    """Add a new member to the library"""
    return db_add_member(first_name, last_name, email, phone, address, membership_number, membership_type)

def update_member(member_id, first_name, last_name, phone, address, membership_type, membership_status):
    """Update an existing member"""
    return db_update_member(member_id, first_name, last_name, phone, address, membership_type, membership_status)

def delete_member(member_id):
    """Delete a member from the library"""
    return db_delete_member(member_id)

def get_all_members():
    """Get all members from the library"""
    return db_get_all_members()

def create_loan(book_id, member_id):
    """Create a new loan"""
    return db_create_loan(book_id, member_id)

def return_loan(loan_id):
    """Return a loan"""
    return db_return_loan(loan_id)

def get_all_loans():
    """Get all loans from the library"""
    return db_get_all_loans()

def update_loan(loan_id, due_date):
    """Update a loan"""
    return db_update_loan(loan_id, due_date)

def delete_loan(loan_id):
    """Delete a loan"""
    return db_delete_loan(loan_id)

def get_library_statistics():
    """Get library statistics"""
    return db_get_library_statistics()