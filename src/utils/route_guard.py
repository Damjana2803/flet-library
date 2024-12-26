from flet_navigator import PageData, ROUTE_404
from utils.global_state import global_state
from components.navbar import navbar

def guests_guard(page_data: PageData, title: str, target_screen, to: str = 'meets'):	
	if not global_state.get_user(): 
		page_data.page.title = title
		page_data.page.add(target_screen(page_data))

	else: 
		page_data.navigate(to)

def auth_guard(page_data: PageData, title: str, target_screen):	
	if global_state.get_user():
		navbar(page_data)
		page_data.page.title = title
		page_data.page.add(target_screen(page_data))

	else:
		page_data.navigate_homepage()

def admin_guard(page_data: PageData, title: str, target_screen):
	user = global_state.get_user()

	if not user or not user['is_admin']:
		page_data.navigate(ROUTE_404)

	else:
		page_data.page.title = title
		page_data.page.add(target_screen(page_data))
