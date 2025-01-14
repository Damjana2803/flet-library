import flet as ft, datetime
from flet_navigator import PageData

def MeetCard(meet, page_data: PageData):
	meet_start_date = datetime.datetime.strptime(meet['meets_start_date'], "%Y-%m-%d").strftime("%d.%m.%Y.")

	return ft.Row(
		expand=True,
		# bgcolor=ft.Colors.RED,
		controls=[
			ft.Container(
				bgcolor=ft.Colors.BLACK,
				content=ft.Column(
					expand=True,
					controls=(
						[
							ft.Container(
								padding=5,
								border_radius=5,
								bgcolor=ft.Colors.GREY_900,
								content=ft.Column(
									[
										ft.Container(
											ft.Text(
												meet['meets_title'],
												overflow=ft.TextOverflow.ELLIPSIS,
												max_lines=1,
												theme_style=ft.TextThemeStyle.LABEL_LARGE
											),
											padding=5
										),
										ft.Container(
											ft.Text(meet['meets_description'], overflow=ft.TextOverflow.FADE, max_lines=1),
											padding=5
										),
										ft.Row(
											[
												ft.Icon(name=ft.Icons.LOCATION_PIN, size=16),
												ft.Text(
													meet['meets_location'],
													theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
													tooltip='Lokacija na kojoj zakazano učenje'
												),
											], 
											alignment=ft.MainAxisAlignment.END,
											spacing=2
										),
										ft.Row(
											[
												ft.Icon(name=ft.Icons.CALENDAR_MONTH, size=16),
												ft.Text(
													meet_start_date,
													theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
													tooltip='Datum kojeg je zakazano učenje'
												),
												ft.Text(
													meet['meets_start_time'],
													theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
													tooltip='Vreme u kome je zakazano učenje'
												)
											], 
											alignment=ft.MainAxisAlignment.END,
											spacing=2
										),
									]
								)
							),
							ft.Row(
								[
									ft.TextButton('Detalji', on_click=lambda _, meet_id=meet['meets_id']: page_data.navigate('meets_show', parameters={'id': meet_id}))
								],
								alignment=ft.MainAxisAlignment.END,
							),
						]
					)
				),
				padding=10,
				border_radius=10,
				expand=True,
			)
		]
	)
	
def MeetShowCard(meet, page_data: PageData):
	meet_start_date = datetime.datetime.strptime(meet['meets_start_date'], "%Y-%m-%d").strftime("%d.%m.%Y.")

	return ft.Container(
		bgcolor=ft.Colors.BLACK,
		content=ft.Column(
			expand=True,
			controls=[
				ft.Text(meet['meets_title'], theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
				ft.Row(
					scroll=ft.ScrollMode.AUTO,
					controls=[
						ft.Container(
							content=ft.Row(
								[
									ft.Icon(ft.Icons.PERSON),
									ft.Text(meet['users_name'], theme_style=ft.TextThemeStyle.BODY_SMALL)
								]
							),
							padding=10,
							border=ft.border.all(1, ft.Colors.BLUE_100),
							border_radius=100
						),
						ft.Container(
							content=ft.Row(
								[
									ft.Icon(ft.Icons.SCHOOL),
									ft.Text(meet['faculty'], theme_style=ft.TextThemeStyle.BODY_SMALL)
								]
							),
							padding=10,
							border=ft.border.all(1, ft.Colors.BLUE_100),
							border_radius=100
						),
						ft.Container(
							content=ft.Row(
								[
									ft.Icon(ft.Icons.TOPIC),
									ft.Text(meet['meets_field'], theme_style=ft.TextThemeStyle.BODY_SMALL)
								]
							),
							padding=10,
							border=ft.border.all(1, ft.Colors.BLUE_100),
							border_radius=100
						),
					]
				),
				ft.Text(meet['meets_description']),
				ft.ResponsiveRow(
					[
						ft.Column(
							controls=[
								ft.Text('Gde?'),
								ft.Row([
									ft.Icon(name=ft.Icons.LOCATION_PIN),
									ft.Text(meet['meets_location'])
								])
							],
							col={'lg': 6}
						),
						ft.Column(
							controls=[
								ft.Text('Kada?'),
								ft.Row([
									ft.Icon(name=ft.Icons.CALENDAR_MONTH),
									ft.Text(
										meet_start_date,
										tooltip='Datum kojeg je zakazano učenje'
									),
									ft.Text(
										meet['meets_start_time'],
										tooltip='Vreme u kome je zakazano učenje'
									)
								])
							],
							col={'lg': 6}
						)
					]
				),
				ft.Row(
					alignment=ft.MainAxisAlignment.END,
					controls=[
						ft.Icon(ft.Icons.PERSON),
						ft.Text(
							f"{meet['user_count']}/{meet['meets_user_limit']}",
							tooltip='Broj korisnika koji se prijavio za ovaj Simpozijum',
						)
					],
				)
			]
		),
		border_radius=10,
		padding=20,
	)
		