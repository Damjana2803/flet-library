import flet as ft
from flet_navigator import PageData

pages = ['home', 'meets', 'profile']

def navbar(page_data: PageData, current_page = 0):
	page = page_data.page
	
	page.navigation_bar = ft.NavigationBar(
		destinations=[
			ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label='Moji Simpozijumi'),
			ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label='Simpozijumi'),
			ft.NavigationBarDestination(
				icon=ft.Icons.BOOKMARK_BORDER,
				selected_icon=ft.Icons.BOOKMARK,
				label='Profil',
			),
		],
		on_change=lambda e: handle_change(e)
	)

	def handle_change(e):
		page_data.navigate(pages[int(e.data)])
