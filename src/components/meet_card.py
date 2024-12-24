import flet as ft, datetime
from flet_navigator import PageData

def MeetCard(meet, page_data: PageData) -> ft.Card:
	meet_start_date = datetime.datetime.strptime(meet['meets_start_date'], "%Y-%m-%d").strftime("%d.%m.%Y.")

	return ft.Card(
		content=ft.Container(
			content=ft.Column(
				[
					ft.ListTile(
						leading=ft.Icon(ft.Icons.ALBUM),
						title=ft.Text(meet['meets_title']),
						subtitle=ft.Column(
							[
								ft.Row(	[
									ft.Text(meet['meets_description'], overflow=ft.TextOverflow.ELLIPSIS)
								]),
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
						[ft.TextButton('Priključi se!'), ft.TextButton('Detalji', on_click=lambda _, meet_id=meet['meets_id']: page_data.navigate('meets_show', parameters={'id': meet_id}))],
						alignment=ft.MainAxisAlignment.END,
					),
				]
			),
			padding=10,
		)
	)


def MeetShowCard(meet, page_data: PageData) -> ft.Card:
	meet_start_date = datetime.datetime.strptime(meet['meets_start_date'], "%Y-%m-%d").strftime("%d.%m.%Y.")

	return ft.Card(
		content=ft.Container(
			content=ft.Column(
				[
					ft.Row(
						[ft.Text(meet['meets_title'], theme_style=ft.TextThemeStyle.HEADLINE_SMALL)]
					),
					ft.Row(
						[
							ft.Container(
								content=ft.Row(
									[
										ft.Icon(ft.Icons.PERSON),
										ft.Text(meet['users_name'], theme_style=ft.TextThemeStyle.BODY_MEDIUM)
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
										ft.Text(meet['faculty'], theme_style=ft.TextThemeStyle.BODY_MEDIUM)
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
										ft.Text(meet['meets_field'], theme_style=ft.TextThemeStyle.BODY_MEDIUM)
									]
								),
								padding=10,
								border=ft.border.all(1, ft.Colors.BLUE_100),
								border_radius=100
							),
						]
					),
					ft.Row(
						[
							ft.Text(meet['meets_description'])
						]
					),
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
				]
			),
			padding=20,
		)
	)