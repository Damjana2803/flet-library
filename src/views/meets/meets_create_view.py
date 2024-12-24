import flet as ft, re, datetime, asyncio
from flet_navigator import PageData
from controllers.meets_controller import handle_create_meet
from components.loader import Loader
from components.responsive_container import ResponsiveContainer

def meets_create_screen(page_data: PageData):
	global selected_date
	global selected_time

	page = page_data.page
	selected_date = datetime.datetime.now()
	selected_time = datetime.datetime.now().time()

	async def on_submit():
		loader = Loader(page)
		asyncio.create_task(loader.create_loader())
		new_meet_id = await handle_create_meet(title_tf.value, description_tf.value, field_tf.value, location_tf.value, selected_date.strftime('%Y-%m-%d'), time_tf.value, limit_tf.value)
		loader.delete_loader()
		
		if new_meet_id == 0: 
			error_snack = ft.SnackBar(ft.Text('Greška prilikom kreiranja Simpozijuma'), duration=2000, open=True)
			page.overlay.append(error_snack)

		else: 
			success_snack = ft.SnackBar(ft.Text('Uspešno kreiran novi Simpozijum'), duration=2000, open=True)
			page.overlay.append(success_snack)
			page_data.navigate('meets_show', parameters={'id': new_meet_id})

		page.update()

	def handle_date_change(e):
		global selected_date
		selected_date = e.control.value
		date_tf.value = e.control.value.strftime('%d.%m.%Y.')
		page.update()

	def handle_time_change(e):
		global selected_time
		selected_time = e.control.value
		time_tf.value = e.control.value.strftime("%H:%M")
		page.update()

	def handle_number_input(e):
		limit_tf.value = re.sub(r'\D', '', limit_tf.value)
		
		page.update()

	title_tf = ft.TextField(label='Naslov Simpozijuma')
	description_tf = ft.TextField(label='Opis Simpozijuma', multiline=True, min_lines=1, max_lines=5)
	field_tf = ft.TextField(label='Naučno polje')
	location_tf = ft.TextField(label='Lokacija održavanja')
	time_tf = ft.TimePicker(help_text='Izaberi vreme održavanja Simpozijuma')
	limit_tf = ft.TextField(label='Slobodna mesta', keyboard_type=ft.KeyboardType.NUMBER, on_change=handle_number_input, max_length=2)
	date_tf = ft.TextField(label='Datum održavanja', value=selected_date.strftime('%d.%m.%Y.'), disabled=True, expand=True)
	time_tf = ft.TextField(label='Vreme održavanja', value=selected_time.strftime("%H:%M"), disabled=True, expand=True)
	
	container = ft.Container(
		ft.Column(
			[
				ft.Row(
					[ ft.Text('Kreiraj novi Simpozijum', theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM) ],
					alignment=ft.MainAxisAlignment.CENTER,
					spacing=10
				),
				title_tf,
				description_tf,
				field_tf,
				location_tf,
				ft.ResponsiveRow(
					[
						ft.Column(
							col={'lg': 6, 'xl': 3},
							controls=[
								ft.Row(
									[
										ft.ElevatedButton(
											'Izaberi datum',
											icon=ft.Icons.CALENDAR_MONTH,
											on_click=lambda e: page.open(
												ft.DatePicker(
													help_text = 'Datum održavanja',
													first_date=datetime.datetime.now(),
													last_date=datetime.datetime.now() + datetime.timedelta(days = 60),
													on_change=handle_date_change,
													value=selected_date
												)
											),
										),
										date_tf
									],
								)
							]
						),
						ft.Column(
							col={'lg': 6, 'xl': 3},
							controls=[
								ft.Row(
									[
										ft.ElevatedButton(
											'Izaberi vreme',
											icon=ft.Icons.CALENDAR_MONTH,
											on_click=lambda e: page.open(
												ft.TimePicker(
														error_invalid_text='Vreme nije validno',
														hour_label_text='H',
														minute_label_text= 'M',
														help_text='Izaberi vreme održavanja',
														on_change=handle_time_change,
														time_picker_entry_mode=ft.TimePickerEntryMode.INPUT,
														value=selected_time
												)
											),
										),
										time_tf
									]
								)
							]
						)
					],
					alignment=ft.MainAxisAlignment.SPACE_AROUND
				),
				limit_tf,
				ResponsiveContainer(
					[
						ft.ElevatedButton(	
							'Kreiraj simpozijum',
							height=50,
							expand=True,
							on_click =  lambda _: asyncio.run(on_submit())
						)
					]
				)
			]
		),
	)

	return ft.SafeArea(container)