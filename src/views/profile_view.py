import flet as ft
from flet_navigator import PageData
from controllers.profile_controller import handle_logout

def profile_screen(page_data: PageData):
	page = page_data.page
	
	def on_logout():
		handle_logout()
		success_snack = ft.SnackBar(ft.Text('Uspešna odjava!'), duration=3000, open=True)
		page.overlay.append(success_snack)
		page_data.navigate_homepage()

	container = ft.Container(
		ft.Column(
			[ ft.ElevatedButton(text="Izloguj se", on_click=lambda _: on_logout())]
		)
	)

	return container