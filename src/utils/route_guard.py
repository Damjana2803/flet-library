from flet_navigator import PageData
from utils.global_state import global_state

def guests_guard(page_data: PageData, title: str, target_screen, to: str = 'home'):	
	if not global_state.get_user(): 
		page_data.page.title = title
		page_data.page.add(target_screen(page_data))

	else: 
		page_data.navigate(to)

def auth_guard(page_data: PageData, title: str, target_screen):	
	if global_state.get_user():
		page_data.page.title = title
		page_data.page.add(target_screen(page_data))

	else:
		page_data.navigate_homepage()

