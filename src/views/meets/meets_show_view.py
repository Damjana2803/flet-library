import flet as ft, asyncio, datetime
from flet_navigator import PageData
from controllers.meets_controller import handle_get_meet, handle_check_if_user_is_signed, handle_toggle_join_user
from components.loader import Loader
from utils.global_state import global_state
from components.meet_card import MeetShowCard
from components.snack_bar import SnackBar
from components.responsive_card import ResponsiveForm

def meets_show_screen(page_data: PageData):
	global meet_data
	
	page = page_data.page
	user = global_state.get_user()
	meet_id = page_data.parameters['id']
	
	join_button = ft.Button(on_click=lambda _: asyncio.run(toggle_join())) 
	column = ft.Column()

	container = ft.Container(
		ResponsiveForm(
			col={ 'md': 10, 'lg': 9, 'xl': 8, 'xxl': 6 },
			controls=[ 
				column 
			]
		),
	)


	async def toggle_join():
		loader = Loader(page)
		asyncio.create_task(loader.create_loader())
		action = await handle_toggle_join_user(user['id'], meet_data['meets_id'])
		loader.delete_loader()
		update_button_text(action['action'])

	def update_button_text(action: str):
		join_button.text = 'Odustani od Simpozijuma' if action == 'INSERT' else 'Priključi se Simpozijumu'
		
		if action == 'INSERT':
			page.overlay.append(
				SnackBar(
					'Uspešno pridruživanje Simpozijumu!', 
					f"On počinje dana {datetime.datetime.strptime(meet_data['meets_start_date'], '%Y-%m-%d').strftime('%d.%m.%Y.')} u {meet_data['meets_start_time']}"
				)
			)
		else:
			page.overlay.append(
				SnackBar(
					'Uspešno otkazivanje tvog dolaska na Simpozijum!',
					snackbar_type='INFO'
				)
			)
		
		page.update()
	
	async def on_mount():
		global meet_data
		
		loader = Loader(page)
		asyncio.create_task(loader.create_loader())
		
		meet_data = await handle_get_meet(meet_id)
		user_is_creator = meet_data['users_id'] == user['id']
		user_is_signed = False 

		if not user_is_creator and not user['is_admin']:
			user_is_signed = await handle_check_if_user_is_signed(user['id'], meet_data['meets_id'])

		loader.delete_loader()
		
		if not meet_data['found']:
			page_data.navigate('not_found')

		page.title = f"Athena | {meet_data['meets_title']}"
		
		column.controls.append(
			ft.Column(
				col={'md': 9, 'lg': 8, 'xl': 7, 'xxl': 6},
				expand=True,
				controls=[MeetShowCard(meet_data, page_data)],
				alignment=ft.MainAxisAlignment.CENTER,
				horizontal_alignment=ft.CrossAxisAlignment.CENTER
			)
		)

		if not user_is_creator and not user['is_admin']:	
			join_button.text = 'Odustani od Simpozijuma' if user_is_signed else 'Priključi se Simpozijumu'
			
			column.controls.append(
				ft.Column(
					col={'md': 9, 'lg': 8, 'xl': 7, 'xxl': 6},
					controls=[
						join_button
					],
					alignment=ft.MainAxisAlignment.CENTER,
					horizontal_alignment=ft.CrossAxisAlignment.CENTER
				)
			)

		page.update()

	asyncio.run(on_mount())
	return ft.SafeArea(container)