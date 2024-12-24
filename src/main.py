import flet as ft
from flet_navigator import VirtualFletNavigator, PublicFletNavigator, PageData, route

from views.login_view import login_screen
from views.register_view import register_screen
from views.home_view import home_screen
from views.profile_view import profile_screen
from views.meets.meets_view import meets_screen
from views.meets.meets_create_view import meets_create_screen

from utils.db import db_init
from utils.route_guard import guests_guard, auth_guard
from views.meets.meets_show_view import meets_show_screen
db_init()

# GUEST ROUTES
@route('/')
def main(page_data: PageData) -> None:
	guests_guard(page_data, 'Athena | Prijava', login_screen)

@route
def register(page_data: PageData) -> None:
	guests_guard(page_data, 'Athena | Registracija', register_screen)

# PROTECTED ROUTES
@route
def home(page_data: PageData) -> None: 
	auth_guard(page_data, 'Athena', home_screen)

@route
def meets(page_data: PageData) -> None:
	auth_guard(page_data, 'Athena | Simpozijumi', meets_screen)
  
@route 
def meets_create(page_data: PageData) -> None:
	auth_guard(page_data, 'Athena | Novi Simpozijum', meets_create_screen)

@route
def meets_show(page_data: PageData) -> None:
	auth_guard(page_data, 'Athena | Simpozijum', meets_show_screen)
	
@route
def profile(page_data: PageData) -> None:
	auth_guard(page_data, 'Athena | Profil', profile_screen)

ft.app(lambda page: PublicFletNavigator(page).render(page))
