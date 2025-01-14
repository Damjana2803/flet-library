import flet as ft, asyncio, re
from flet_navigator import PageData
from controllers.admin_controller import handle_get_all_meets, delete_meet
from components.loader import Loader
from components.tab_bar import TabBar
from components.table import Table
from components.snack_bar import SnackBar

def admin_meets_screen(page_data: PageData):
	global rows
	global selected_id
	page = page_data.page
	rows = []

	def handle_number_input(e):
		limit_tf.value = re.sub(r'\D', '', limit_tf.value)

	title_tf = ft.TextField(label='Naslov Simpozijuma')
	desc_tf = ft.TextField(label='Opis Simpozijuma', multiline=True, max_lines=10)
	limit_tf = ft.TextField(label='Slobodna mesta', keyboard_type=ft.KeyboardType.NUMBER, on_change=handle_number_input, max_length=2)

	edit_modal = ft.AlertDialog(
		modal=True,
		title=ft.Text("Uredite Simpozijum"),
		content=ft.Column(
			width=500,
			height=500,
			expand=True,
			controls=[
				title_tf,
				desc_tf,
				limit_tf
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
		title=ft.Text(f"Obrisaćete Simpozijum"),
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

	async def handle_edit():
		global selected_id

	async def handle_delete():
		global selected_id

		is_deleted = await delete_meet(rows[selected_id]['meets_id'])

		if is_deleted:
			page.overlay.append(SnackBar('Uspešno ste obrisali Simpozijum', duration=2500))
			handle_close('DELETE')
		else:
			page.overlay.append(SnackBar('Greška prilikom brisanja Simpozijuma', snackbar_type='ERROR'))

		page.update()

		
	

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
			title_tf.value = rows[selected_id]['meets_title']
			desc_tf.value = rows[selected_id]['meets_description']
			limit_tf.value = rows[selected_id]['meets_users_limit']
			page.open(edit_modal)
		elif modal == 'DELETE':
			page.open(delete_modal)


	async def on_mount():
		global rows 
		loader = Loader(page)
		asyncio.create_task(loader.create_loader())
		rows = await  handle_get_all_meets()
		loader.delete_loader()

		table = Table(
			col_names=['Naslov', 'Oblast', 'Datum i vreme', 'Lokacija', 'Akcije'],
			col_keys=['meets_title', 'meets_field', 'meets_start_date', 'meets_location', 'TABLE.ACTIONS'],
			on_edit=handle_open,
			on_delete=handle_open,
			rows=rows
		)

		row.controls.append(table)

		page.update()

	row = ft.Column(
		[
			TabBar(
				page_data=page_data,
				tab_urls=['admin', 'admin_meets'],
				tab_titles=['Korisnici', 'Simpozijumi'],
				tab_func=[lambda _: page_data.navigate('admin'), lambda _: page_data.navigate('admin_meets'),]
			)
		]
	)

	asyncio.run(on_mount())

	return ft.SafeArea(
		ft.Container(
			row
		)
	)
		
		