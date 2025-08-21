from flet_navigator import PageData
from components.navbar import navbar
from utils.session_manager import get_current_user, is_admin
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def guests_guard(page_data: PageData, title: str, target_screen, to: str = 'meets'):	
	user = get_current_user()
	
	if not user: 
		page_data.page.title = title
		page_data.page.add(target_screen(page_data))
	else: 
		page_data.navigate(to)

def auth_guard(page_data: PageData, title: str, target_screen):	
	user = get_current_user()
	
	if user:
		navbar(page_data)
		page_data.page.title = title
		page_data.page.add(target_screen(page_data))
	else:
		page_data.navigate_homepage()

def admin_guard(page_data: PageData, title: str, target_screen):
	user = get_current_user()
	print(f"Admin guard - user: {user}")

	if not user or not is_admin():
		print(f"User not admin, redirecting to 404. User: {user}")
		page_data.navigate('error_404_route')
	else:
		print(f"User is admin, proceeding to {title}")
		page_data.page.title = title
		page_data.page.add(target_screen(page_data))
