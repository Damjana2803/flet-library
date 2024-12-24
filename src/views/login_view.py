import flet as ft, asyncio
# from components.button import form_button
from flet_navigator import PageData
from controllers.login_controller import handle_login
from components.loader import Loader
from components.responsive_container import ResponsiveContainer

def login_screen(page_data: PageData) -> None:  
	page = page_data.page
	page.navigation_bar = None
	
	async def on_submit():
		if (len(email_tf.value) != 0 and len(password_tf.value) != 0):
			loader = Loader(page)
			asyncio.create_task(loader.create_loader())
			logged_in = handle_login(email_tf.value, password_tf.value)
			loader.delete_loader()
			
			if logged_in:
				# login is successful
				success_snack = ft.SnackBar(ft.Text('Uspešna prijava!'), duration=2000, open=True)
				page.overlay.append(success_snack)
				page_data.navigate('meets')

			else: 
				# login is not succesful
				error_snack = ft.SnackBar(
					ft.Column(
						[
							ft.Text('Greška prilikom prijave', weight=ft.FontWeight.BOLD), 
							ft.Text('Uneta je netačna e-adresa i/ili lozinka')
						]
					),
					duration=2000,
					open=True
				)
				email_tf.border_color = ft.Colors.RED_300
				password_tf.border_color = ft.Colors.RED_300
				page.overlay.append(error_snack)

			page.update()
	
	email_tf = ft.TextField(
		label='E-adresa',
		prefix_icon=ft.Icons.EMAIL,
		keyboard_type=ft.KeyboardType.EMAIL,
		autofill_hints=ft.AutofillHint.EMAIL
	)
	password_tf = ft.TextField(
		label='Lozinka',
		password=True,
		can_reveal_password=True,
		prefix_icon=ft.Icons.LOCK,
		autofill_hints=ft.AutofillHint.PASSWORD
	)

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
    
				ResponsiveContainer(
					[ 
						ft.ElevatedButton(
							'Prijavi se',
							expand=True,
							height=50,
							on_click = lambda _: asyncio.run(on_submit()),
						) 
					],
				),

				ft.Row(
					[ 
						ft.TextButton(
							'Nemaš nalog? Registruj se',
							on_click=lambda _: page_data.navigate('register'),
						)
					]
				)
			]
		)
	)

	return container
