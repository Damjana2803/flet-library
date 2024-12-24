import flet as ft
from flet_navigator import PageData
from controllers.profile_controller import handle_logout
from utils.global_state import global_state

def profile_screen(page_data: PageData):
	page = page_data.page
	user = global_state.get_user()

	def on_logout():
		handle_logout()
		success_snack = ft.SnackBar(ft.Text('Uspešna odjava!'), duration=3000, open=True)
		page.overlay.append(success_snack)
		page_data.navigate_homepage()

	is_admin = ft.Row()

	if user['is_admin']:
		is_admin.controls.append(
			ft.Button(
				text="Admin",
				icon=ft.Icons.ADD,
				height=50,
				elevation=0,
				expand=True,
				on_click=lambda _: on_logout()
			)
		)

	container = ft.Container(
		ft.ResponsiveRow(
			[ 
				ft.Column(
					col={'md': 6, 'lg': 5, 'xl': 4},
					controls=[
						ft.Row(
							[
								ft.Icon(
									name=ft.Icons.PERSON,
									expand=True,
									size=48,
								),
							]
						),
						ft.Row(
							[
								ft.Text(
									user['name'],
									text_align=ft.TextAlign.CENTER,
									expand=True,
									theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM
								)
							]
						),
						is_admin,
						ft.Row(
							[
								ft.Button(
									text="Izloguj se",
									icon=ft.Icons.ADD,
									height=50,
									elevation=0,
									expand=True,
									on_click=lambda _: on_logout()
								)
							]
						)
					],
					alignment=ft.MainAxisAlignment.CENTER
				),
			],
			alignment=ft.MainAxisAlignment.CENTER
		)
	)

	return ft.SafeArea(container)
