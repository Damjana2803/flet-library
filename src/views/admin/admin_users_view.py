import flet as ft, asyncio
from flet_navigator import PageData
from components.loader import Loader
from controllers.admin_controller import get_all_users
from utils.helper_func import faculties_options
from components.table import Table

def admin_users_screen(page_data: PageData):
	global rows
	global selected_id 

	page = page_data.page
	rows = []

	email_tf = ft.TextField(label='E-adresa korisnika', disabled=True)
	name_tf = ft.TextField(label='Ime korisnika')
	faculty_tf = ft.Dropdown(options=faculties_options(), label='Fakultet korisnika')

	def handle_close(modal):
		global selected_id
		selected_id = None

		if(modal == 'EDIT'):
			page.close(edit_modal)
		elif(modal == 'DELETE'):
			page.close(delete_modal)

	def handle_open(id, modal):
		global selected_id
		selected_id = id

		if(modal == 'EDIT'):
			name_tf.value = rows[selected_id]['name']
			faculty_tf.value = rows[selected_id]['faculty']
			email_tf.value = rows[selected_id]['email']
			page.open(edit_modal)
		elif(modal == 'DELETE'):
			page.open(delete_modal)

	def handle_delete():
		global selected_id
		print(selected_id, 'DELETED!')

	def handle_edit():
		global selected_id
		print(selected_id, 'EDITED!')

	edit_modal = ft.AlertDialog(
		modal=True,
		title=ft.Text("Uredite informacije korisnika"),
		content=ft.Column(
			expand=True,
			height=160,
			controls=[
				email_tf,
				name_tf,
				faculty_tf,
			]
		),
		actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
		actions=[
				ft.TextButton("Odbaci", on_click=lambda _: handle_close('EDIT')),
				ft.TextButton("Sačuvaj", on_click=lambda _: handle_edit()),
		],
	)

	delete_modal = ft.AlertDialog(
		modal=True,
		title=ft.Text(f"Obrisaćete korisnika"),
		content=ft.Text("Ova akcija je permanentna. Da li ste sigurni?"),
		actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
		adaptive=True,
		inset_padding=ft.padding.symmetric(vertical=20, horizontal=12),
		actions=[
				ft.TextButton('Ne, nisam siguran', on_click=lambda _: handle_close('DELETE'), expand=True),
				ft.TextButton(
					'Da',
					style=ft.ButtonStyle(
						bgcolor=ft.Colors.RED_500
					),
					on_click=lambda _: handle_delete()
				)
		]
	)


	table = Table(['Ime', 'E-adresa', 'Fakultet', 'Akcije'])
	row = ft.Column(
		controls=[
			table
		]
	)

	async def on_mount():
		global rows 
		loader = Loader(page)
		asyncio.create_task(loader.create_loader())
		rows = await get_all_users()
		loader.delete_loader()

		# row.controls = [
		# 	ft.Text('HELLO NIGGA'),
		# 	ft.IconButton(
		# 		icon=ft.Icons.EDIT, 
		# 		on_click=lambda _, id = rows[0]['id']: handle_open(id, 'EDIT')
		# 	),
		# 	ft.IconButton(
		# 		icon=ft.Icons.DELETE, 
		# 		on_click=lambda _, id = rows[0]['id']: handle_open(id, 'DELETE')
		# 	)
		# ]
		# page.update()

	asyncio.run(on_mount())

	return ft.SafeArea(
		ft.Container(
			row
		)
	)