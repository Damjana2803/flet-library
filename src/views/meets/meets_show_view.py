import flet as ft, asyncio
from flet_navigator import PageData
from controllers.meets_controller import handle_get_meet, handle_check_if_user_is_signed, handle_toggle_join_user
from components.loader import Loader
from utils.global_state import global_state
from components.meet_card import MeetShowCard

def meets_show_screen(page_data: PageData):
	global meet_data
	page = page_data.page
	user_id = global_state.get_user()['id']
	meet_id = page_data.parameters['id']
	
	column = ft.Column()

	container = ft.SafeArea(
		ft.Container(
			ft.ResponsiveRow([ column ]),
		)
	)

	async def toggle_join():
		loader = Loader(page)
		asyncio.create_task(loader.create_loader())
		await handle_toggle_join_user(user_id, meet_data['meets_id'])
		loader.delete_loader()
		page.update()

	async def on_mount():
		global meet_data
		
		loader = Loader(page)
		asyncio.create_task(loader.create_loader())
		
		meet_data = await handle_get_meet(meet_id)
		user_is_creator = meet_data['users_id'] == user_id
		user_is_signed = False 

		if(user_is_creator == False):
			user_is_signed = await handle_check_if_user_is_signed(user_id, meet_data['meets_id'])

		loader.delete_loader()



		print(user_is_creator, user_is_signed)
		
		if meet_data['found'] == False:
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

		# OVO MORA U POSEBNU FUNKCIJU!!! ZBOG RE-RENDEROVANJA
		if user_is_creator == False:
			button_text = 'Odustani od Simpozijuma' if user_is_signed else 'Priključi se Simpozijumu'
			column.controls.append(
				ft.Column(
					col={'md': 9, 'lg': 8, 'xl': 7, 'xxl': 6},
					controls=[
						ft.Button(button_text, on_click=lambda _: asyncio.run(toggle_join())) 
					],
					alignment=ft.MainAxisAlignment.CENTER,
					horizontal_alignment=ft.CrossAxisAlignment.CENTER
				)
			)

		page.update()

	asyncio.run(on_mount())
	return container