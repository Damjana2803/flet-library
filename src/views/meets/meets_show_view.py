import flet as ft, asyncio, datetime
from flet_navigator import PageData
from controllers.meets_controller import handle_get_meet, handle_check_if_user_is_signed, handle_toggle_join_user, handle_add_comment, handle_get_users_in_meet
from components.loader import Loader
from utils.global_state import global_state
from components.meet_card import MeetShowCard
from components.snack_bar import SnackBar
from components.responsive_card import ResponsiveForm
from components.modals.rate_modal import RateModal

def meets_show_screen(page_data: PageData):
	global meet_data
	
	page = page_data.page
	user = global_state.get_user()
	meet_id = page_data.parameters['id']
	

	join_button = ft.Button(
		on_click=lambda _: asyncio.run(toggle_join()),
		expand=True,
		height=50
	) 

	async def save_comment(rating, comment):
		success = asyncio.create_task(handle_add_comment(user['id'], meet_id, rating, comment))

		if success:
			page.overlay.append(
				SnackBar('Uspešno ostavljena recenzija!')
			)

		else: 
			page.overlay.append(
				SnackBar('Greška prilikom ostavljanja recenzije!', type='ERROR')
			)

		page.update()

	def close_rate_modal(e=None):
		if rate_modal in page.overlay:
			rate_modal.open = False
			page.update()

	def show_rate_modal():
		if rate_modal not in page.overlay:
			page.overlay.append(rate_modal)
		
		rate_modal.open = True
		page.update()

	rate_modal = RateModal(
		title='Oceni Simpozijum',
		page=page,
		on_save=save_comment,
		on_close=close_rate_modal
	)

	rate_button = ft.Button(
		'Oceni Simpozijum',
		on_click=lambda _: show_rate_modal(),
		expand=True,
		height=50
	)

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
		users_joined = []

		if not user_is_creator and not user['is_admin']:
			user_is_signed = await handle_check_if_user_is_signed(user['id'], meet_data['meets_id'])

		else:
			users_joined = await handle_get_users_in_meet(meet_id)

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

		# TODO: check if date is in the past -> if it is show 'add comment' button if joined...
		# if already commented, then remove the button :/
		# if creator/admin -> see all comments and stars :P
		present = datetime.datetime.now()
		str_date = ' '.join((meet_data['meets_start_date'], meet_data['meets_start_time']))
		meet_date = datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M")

		if not user_is_creator and not user['is_admin']:	
			if present < meet_date:
				join_button.text = 'Odustani od Simpozijuma' if user_is_signed else 'Priključi se Simpozijumu'
				
				column.controls.append(
					ft.Row([ join_button ])
				)
			
			else:
				# TODO: add check here if user has already commented...
				column.controls.append(
					ft.Row([ rate_button ])
				)

		if user_is_creator or user['is_admin']:
			if present < meet_date:
				column.controls.append(
					ft.Row(
						[ 
							ft.ElevatedButton(
								'Upravljaj Simpozijumom',
								height=50,
								expand=True
							)
						]
					)
				)

			users_column = ft.Column()
			
			if len(users_joined):
				users_column.controls.append(
					ft.Text('Korisnici', theme_style=ft.TextThemeStyle.HEADLINE_SMALL)
				)

			for user_joined in users_joined:
				users_column.controls.append(
					ft.Container(
						content=ft.Row([
							ft.Icon(name=ft.Icons.PERSON_2),
							ft.Text(user_joined['users_name']),
							ft.Text(user_joined['users_email'])
						])
					)
				)

			
				if present > meet_date:
					if user_joined['rating'] is not None:
						stars_row = ft.Row()
						users_column.controls.append(
							ft.Container(
								content=stars_row,
								margin=ft.margin.only(left=20)
							)
						)

						for i in range(5):
							stars_row.controls.append(
								ft.Icon(
									name=ft.Icons.STAR if i < user_joined['rating'] else ft.Icons.STAR_BORDER,
									size=16
								)
							) 
					if user_joined['comment'] is not None:
						users_column.controls.append(
							ft.Container(
								content=ft.Text(user_joined["comment"]),
								margin=ft.margin.only(left=20)
							)
						)

			column.controls.append(
				users_column
			)

		page.update()

	asyncio.run(on_mount())
	return ft.SafeArea(container)