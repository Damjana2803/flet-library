import flet as ft
from flet_navigator import PublicFletNavigator, PageData, route

# Import library views
from views.login_view import login_screen
from views.register_view import register_screen

# Import admin views
from views.admin.admin_dashboard import admin_dashboard as admin_dashboard_content
from views.admin.admin_books import admin_books as admin_books_content
from views.admin.admin_members import admin_members as admin_members_content
from views.admin.admin_loans import admin_loans as admin_loans_content
from views.admin.admin_statistics import admin_statistics as admin_statistics_content

# Import member views
from views.member_dashboard import member_dashboard_screen as member_dashboard_content
from views.book_search import book_search as book_search_content
from views.my_loans import my_loans as my_loans_content
from views.my_reservations import my_reservations as my_reservations_content
from views.member_profile import member_profile as member_profile_content

from utils.db import db_init
from utils.route_guard import guests_guard, auth_guard, admin_guard

db_init()

# GUEST ROUTES
@route('/')
def main(page_data: PageData) -> None:
	guests_guard(page_data, 'Biblioteka | Prijava', login_screen)

@route
def login(page_data: PageData) -> None:
	guests_guard(page_data, 'Biblioteka | Prijava', login_screen)

@route
def register(page_data: PageData) -> None:
	guests_guard(page_data, 'Biblioteka | Registracija člana', register_screen)

# ADMIN ROUTES
@route
def admin_dashboard(page_data: PageData) -> None:
	admin_guard(page_data, 'Biblioteka Admin | Dashboard', lambda pd: admin_dashboard_content(pd))

@route
def admin_books(page_data: PageData) -> None:
	admin_guard(page_data, 'Biblioteka Admin | Upravljanje knjigama', lambda pd: admin_books_content(pd))

@route
def admin_members(page_data: PageData) -> None:
	admin_guard(page_data, 'Biblioteka Admin | Upravljanje članovima', lambda pd: admin_members_content(pd))

@route
def admin_loans(page_data: PageData) -> None:
	admin_guard(page_data, 'Biblioteka Admin | Iznajmljivanje', lambda pd: admin_loans_content(pd))

@route
def admin_statistics(page_data: PageData) -> None:
	admin_guard(page_data, 'Biblioteka Admin | Statistike', lambda pd: admin_statistics_content(pd))

# MEMBER ROUTES
@route
def member_dashboard(page_data: PageData) -> None:
	auth_guard(page_data, 'Biblioteka | Dashboard', lambda pd: member_dashboard_content(pd))

@route
def book_search(page_data: PageData) -> None:
	auth_guard(page_data, 'Biblioteka | Pretraga knjiga', lambda pd: book_search_content(pd))

@route
def my_loans(page_data: PageData) -> None:
	auth_guard(page_data, 'Biblioteka | Moje iznajmljene knjige', lambda pd: my_loans_content(pd))

@route
def my_reservations(page_data: PageData) -> None:
	auth_guard(page_data, 'Biblioteka | Moje rezervacije', lambda pd: my_reservations_content(pd))

@route
def member_profile(page_data: PageData) -> None:
	auth_guard(page_data, 'Biblioteka | Moj profil', lambda pd: member_profile_content(pd))

ft.app(
    lambda page: PublicFletNavigator(page).render(page)
)
