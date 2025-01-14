import flet as ft, asyncio
from flet_navigator import PageData
from utils.helper_func import faculties_options
from controllers.admin_controller import get_all_users, edit_user, delete_user
from components.loader import Loader
from components.table import Table
from components.snack_bar import SnackBar
from components.tab_bar import TabBar

def admin_users_screen(page_data: PageData):
	global rows
	global selected_id 

	page = page_data.page
	rows = []

	email_tf = ft.TextField(label='E-adresa korisnika', disabled=True)
	name_tf = ft.TextField(label='Ime korisnika')
	faculty_dropdown = ft.Dropdown(options=faculties_options(), label='Fakultet korisnika')

	def handle_close(modal):
		global selected_id
		selected_id = None

		if modal == 'EDIT':
			page.close(edit_modal)
		elif modal == 'DELETE':
			page.close(delete_modal)

	def handle_open(id, modal):
		global selected_id
		selected_id = id

		if modal == 'EDIT':
			name_tf.value = rows[selected_id]['name']
			faculty_dropdown.value = rows[selected_id]['faculty']
			email_tf.value = rows[selected_id]['email']
			page.open(edit_modal)
		elif modal == 'DELETE':
			page.open(delete_modal)

	async def handle_delete():
		global selected_id
		
		is_deleted = await delete_user(rows[selected_id]['id'])

		if is_deleted:
			page.overlay.append(SnackBar('Uspešno ste obrisali korisnika', f"Korisnik sa e-adresom {rows[selected_id]['email']} je uspešno obrisan", duration=2500))
			handle_close('DELETE')
		else:
			page.overlay.append(SnackBar('Greška prilikom brisanja korisnika', snackbar_type='ERROR'))
		
		page.update()
		

	async def handle_edit():
		global selected_id
		email_tf.border_color = None
		name_tf.border_color = None
		faculty_dropdown.border_color = None

		field_controls = {
			'email': email_tf,
			'name': name_tf,
			'faculty': faculty_dropdown,
		}
		# loader = Loader(page)
		# asyncio.create_task(loader.create_loader())		
		edit = await edit_user(rows[selected_id]['id'], name_tf.value, faculty_dropdown.value)
		# loader.delete_loader()

		if edit['success']:
			page.overlay.append(SnackBar('Uspešno ste izmenili korisnika', f"Korisnik sa e-adresom {rows[selected_id]['email']} je uspešno izmenjen", duration=2500))
			handle_close('EDIT')
		else:
			error_snack = SnackBar('Greška prilikom ažuriranja korisnika', snackbar_type='ERROR')
			
			for error in edit['errors']:
				if error['field'] in field_controls:
					field_controls[error['field']].border_color = ft.Colors.RED_300

				error_snack.append_error(error['message'])
				
			page.overlay.append(error_snack)

		page.update()

	edit_modal = ft.AlertDialog(
		modal=True,
		title=ft.Text("Uredite informacije korisnika"),
		content=ft.Column(
			expand=True,
			height=160,
			controls=[
				email_tf,
				name_tf,
				faculty_dropdown,
			]
		),
		actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
		actions=[
				ft.TextButton("Odbaci", on_click=lambda _: handle_close('EDIT')),
				ft.TextButton("Sačuvaj", on_click=lambda _: asyncio.run(handle_edit())),
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
					on_click=lambda _: asyncio.run(handle_delete())
				)
		]
	)

	row = ft.Column(controls=[
		TabBar(
			page_data=page_data,
			tab_urls=['admin', 'admin_meets'],
			tab_titles=['Korisnici', 'Simpozijumi'],
			tab_func=[lambda _: page_data.navigate('admin'), lambda _: page_data.navigate('admin_meets'),]
		)
	])

	async def on_mount():
		global rows 
		loader = Loader(page)
		asyncio.create_task(loader.create_loader())
		rows = await get_all_users()
		loader.delete_loader()

		table = Table(
			col_names=['Ime', 'E-adresa', 'Fakultet', 'Akcije'],
			col_keys=['name', 'email', 'faculty', 'TABLE.ACTIONS'],
			ignore_key='is_admin',
			on_edit=handle_open,
			on_delete=handle_open,
			rows=rows
		)
		
		row.controls.append(table)

		page.update()

	asyncio.run(on_mount())

	return ft.SafeArea(
		ft.Container(
			row
		)
	)