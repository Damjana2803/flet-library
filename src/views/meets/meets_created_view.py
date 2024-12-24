import flet as ft, asyncio
from flet_navigator import PageData
from components.loader import Loader
from utils.global_state import global_state
from controllers.meets_controller import handle_get_all_created_meets
from components.meet_card import MeetCard
from components.responsive_container import ResponsiveContainer
from components.responsive_container import ResponsiveContainer

def meets_created_view(page_data: PageData):
	global meets_data
	user_id = global_state.get_user()['id']
	page = page_data.page
	page.scroll = ft.ScrollMode.AUTO
	page.horizontal_alignment = 'center'
	
	column = ft.Column(
		horizontal_alignment='center',
		controls=[
			ResponsiveContainer(
				col={'md': 6, 'lg': 4},
				alignment=ft.MainAxisAlignment.END,
				controls=[
					ft.SearchBar(
						bar_hint_text="Traži Simpozijume...",
						bar_leading=ft.IconButton(icon=ft.Icons.SEARCH),
						expand=True,
						height=50,
					)
				]
			),
			ResponsiveContainer(
				[
					ft.Button(
						text="Kreiraj novi Simpozijum",
						icon=ft.Icons.ADD,
						height=50,
						elevation=0,
						expand=True,
						on_click=lambda _: page_data.navigate('meets_create'),
					)
				]
			)
		]
	)
	
	row = ft.ResponsiveRow(
		controls=[],
		spacing=10
	)

	container = ft.SafeArea(
		ft.Container(
			ft.Column(
				[
					column,
					row
				]
			)
		)
	)

	async def on_mount():
		global meets_data 
		loader = Loader(page)
		asyncio.create_task(loader.create_loader())
		meets_data = await handle_get_all_created_meets(user_id)
		loader.delete_loader()
		
		for meet in meets_data:
			row.controls.append(
				ft.Column(
					expand=True,
					col={'md': 6, 'lg': 3},
					controls=[MeetCard(meet, page_data)]
				)
			)

			page.update()

	asyncio.run(on_mount())
	return container