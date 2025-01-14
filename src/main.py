import flet as ft
from flet_navigator import PublicFletNavigator, PageData, route

from views.login_view import login_screen
from views.register_view import register_screen
from views.profile_view import profile_screen
from views.meets.meets_view import meets_screen
from views.meets.meets_create_view import meets_create_screen
from views.meets.meets_show_view import meets_show_screen
from views.meets.meets_created_view import meets_created_screen
from views.admin.admin_users_view import admin_users_screen
from views.admin.admin_meets_view import admin_meets_screen
from views.meets.meets_joined_view import meets_joined_screen

from utils.db import db_init
from utils.route_guard import guests_guard, auth_guard, admin_guard

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
def meets_created(page_data: PageData) -> None:
	auth_guard(page_data, 'Athena | Moji Simpozijumi', meets_created_screen)

@route
def meets_joined(page_data: PageData) -> None:
	auth_guard(page_data, 'Athena | Pridruženi Simpozijumi', meets_joined_screen)

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

# ADMIN ROUTES
@route
def admin(page_data: PageData) -> None:
	admin_guard(page_data, 'Athena Admin | Korisnici', admin_users_screen)

@route 
def admin_meets(page_data: PageData) -> None:
	admin_guard(page_data, 'Athena Admin | Simpozijumi', admin_meets_screen)



ft.app(lambda page: PublicFletNavigator(page).render(page))
