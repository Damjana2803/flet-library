import flet as ft, asyncio
from flet_navigator import PageData
from controllers.login_controller import register_user
from components.loader import Loader
from components.responsive_card import ResponsiveForm
from components.snack_bar import SnackBar

def register_screen(page_data: PageData):
	page = page_data.page
	page.title = "Registracija - Biblioteka"
	
	async def on_submit():
		loader = Loader(page)
		asyncio.create_task(loader.create_loader())		
		
		register = register_user(
			email=email_tf.value,
			password=password_tf.value,
			first_name=first_name_tf.value,
			last_name=last_name_tf.value,
			phone=phone_tf.value,
			address=address_tf.value,
			membership_type=membership_type.value
		)
		
		loader.delete_loader()

		if register[0]:  # Success
			page.overlay.append(SnackBar('Uspešna registracija', 'Premeštam te na stranicu za prijavu...', duration=2500))
			page_data.navigate('/')

		else: 
			# Reset border colors
			email_tf.border_color = None
			first_name_tf.border_color = None
			last_name_tf.border_color = None
			password_tf.border_color = None
			phone_tf.border_color = None
			address_tf.border_color = None
			membership_type.border_color = None

			error_snack = SnackBar('Greška prilikom registracije', snackbar_type='ERROR')
			error_snack.append_error(register[1])  # Error message
			page.overlay.append(error_snack)
	
		page.update()

	email_tf = ft.TextField(
		prefix_icon=ft.Icons.EMAIL,
		label='E-adresa *',
		autofill_hints=ft.AutofillHint.EMAIL,
		keyboard_type=ft.KeyboardType.EMAIL,
		hint_text="Unesite vašu e-adresu"
	)

	first_name_tf = ft.TextField(
		prefix_icon=ft.Icons.PERSON,
		label='Ime *',
		hint_text="Unesite vaše ime"
	)

	last_name_tf = ft.TextField(
		prefix_icon=ft.Icons.PERSON,
		label='Prezime *',
		hint_text="Unesite vaše prezime"
	)

	password_tf = ft.TextField(
		prefix_icon=ft.Icons.LOCK,
		label='Lozinka *',
		password=True,
		can_reveal_password=True,
		autofill_hints=ft.AutofillHint.NEW_PASSWORD,
		helper_text='Najmanje 6 karaktera',
		hint_text="Unesite lozinku"
	)
	
	phone_tf = ft.TextField(
		prefix_icon=ft.Icons.PHONE,
		label='Broj telefona *',
		keyboard_type=ft.KeyboardType.PHONE,
		hint_text="Unesite broj telefona"
	)
	
	address_tf = ft.TextField(
		prefix_icon=ft.Icons.LOCATION_ON,
		label='Adresa *',
		multiline=True,
		min_lines=2,
		max_lines=3,
		hint_text="Unesite vašu adresu"
	)
	
	membership_type = ft.Dropdown(
		prefix_icon=ft.Icons.CARD_MEMBERSHIP,
		label='Tip članstva *',
		hint_text='Izaberite tip članstva',
		helper_text='Studentski: 3 knjige, Regularni: 5 knjiga, Penzionerski: 7 knjiga',
		options=[
			ft.dropdown.Option('student', 'Studentski'),
			ft.dropdown.Option('regular', 'Regularni'),
			ft.dropdown.Option('senior', 'Penzionerski'),
		],
	)

	container = ft.SafeArea(
		ResponsiveForm(
			[
				ft.Row(
					[ft.Text('Registracija člana', theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
					alignment=ft.MainAxisAlignment.CENTER,
				),
				ft.Text(
					'Postanite član naše biblioteke',
					theme_style=ft.TextThemeStyle.BODY_MEDIUM,
					color=ft.Colors.GREY_600,
					text_align=ft.TextAlign.CENTER
				),
				ft.Column(
					[ 
						email_tf, 
						first_name_tf, 
						last_name_tf, 
						password_tf, 
						phone_tf, 
						address_tf, 
						membership_type 
					]
				),
				ft.Row(
					[ 
						ft.ElevatedButton(
							'Registruj se kao član', 
							on_click = lambda _: asyncio.run(on_submit()),
							height=50,
							expand=True,
							icon=ft.Icons.PERSON_ADD
						) 
					],
				),
				ft.Row(
					[ ft.TextButton('Imaš nalog? Prijavi se', on_click=lambda _: page_data.navigate('/')) ]
				)
			]
		)
	)

	return container