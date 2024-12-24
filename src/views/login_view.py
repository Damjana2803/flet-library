import flet as ft
# from components.button import form_button
from flet_navigator import PageData
from controllers.login_controller import handle_login

def login_screen(page_data: PageData) -> None:  
	page = page_data.page

	def on_submit():
		if (len(email_tf.value) != 0 and len(password_tf.value) != 0):
			if handle_login(email_tf.value, password_tf.value):
				# login is successful
				success_snack = ft.SnackBar(ft.Text('Uspešna prijava!'), duration=2000, open=True)
				page.overlay.append(success_snack)
				page_data.navigate('home')

			else: 
				# login is not succesful
				error_snack = ft.SnackBar(ft.Text('Greška prilikom prijave: uneta je netačna e-adresa i/ili lozinka'), duration=2000, open=True)
				email_tf.border_color = ft.Colors.RED_300
				password_tf.border_color = ft.Colors.RED_300
				page.overlay.append(error_snack)

			page.update()
	
	email_tf = ft.TextField(label='E-adresa', prefix_icon=ft.Icons.EMAIL)
	password_tf = ft.TextField(label='Lozinka', password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK)

	container = ft.Container(
		ft.Column(
			[
				ft.Row(
					[ft.Text("Prijava", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
					alignment=ft.MainAxisAlignment.CENTER,
				),
				ft.Column(
					[ email_tf, password_tf ]
				),
    
				ft.Row(
					[ ft.ElevatedButton('Prijavi se', on_click = lambda _: on_submit()) ],
					alignment=ft.MainAxisAlignment.CENTER
				),
				ft.Row(
					[ ft.TextButton('Nemaš nalog? Registruj se', on_click=lambda _: page_data.navigate('register'))]
				)
			]
		)
	)

	return container
