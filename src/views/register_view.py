import flet as ft
from flet_navigator import PageData
from controllers.register_controller import handle_register

def register_screen(page_data: PageData):
	def on_submit():
		handle_register(email_tf.value, name_tf.value, password_tf.value, faculty.value)
  
	email_tf = ft.TextField(label='E-adresa')
	name_tf = ft.TextField(label='Ime i prezime')
	password_tf = ft.TextField(label='Lozinka', password=True, can_reveal_password=True)
	faculty = ft.Dropdown(
		label='Fakultet',
		hint_text='Izaberi tvoj fakultet',
		options=[
				ft.dropdown.Option('Ekonomski fakultet'),
				ft.dropdown.Option('Medicinski fakultet'),
				ft.dropdown.Option('Poljoprivredni fakultet'),
				ft.dropdown.Option('Pravni fakultet'),
				ft.dropdown.Option('Prirodno-matematički fakultet'),
				ft.dropdown.Option('Učiteljski fakultet'),
				ft.dropdown.Option('Fakultet za sport i fizičko vaspitanje'),
				ft.dropdown.Option('Fakultet tehničkih nauka'),
				ft.dropdown.Option('Filozofski fakultet'),
		],
	)

	container = ft.Container(
		ft.Column(
			[
				ft.Row(
					[ft.Text('Registracija', theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
					alignment=ft.MainAxisAlignment.CENTER,
				),
				ft.Column(
					[ email_tf, password_tf, name_tf, faculty ]
				),
				ft.Row(
					[ ft.ElevatedButton('Registruj se', on_click = lambda _: on_submit()) ],
					alignment=ft.MainAxisAlignment.CENTER
				),
				ft.Row(
					[ ft.TextButton('Imaš nalog? Prijavi se', on_click=lambda _: page_data.navigate('/')) ]
				)
			]
		)
	)
 
	return container