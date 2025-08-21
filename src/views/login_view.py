import flet as ft, asyncio
# from components.button import form_button
from flet_navigator import PageData
from controllers.login_controller import login_user
from components.loader import Loader
from components.responsive_card import ResponsiveForm
from components.snack_bar import SnackBar
from utils.session_manager import set_current_user

def login_screen(page_data: PageData) -> None:  
	page = page_data.page
	page.navigation_bar = None
	
	def on_submit():
		if (len(email_tf.value) != 0 and len(password_tf.value) != 0):
			# Determine login type based on radio button selection
			login_type = user_type_group.value
			
			success, message, user_data = login_user(email_tf.value, password_tf.value)
			
			if success:
				# login is successful
				user_type = "Administrator" if user_data.get('is_admin', False) else "Član"
				page.overlay.append(SnackBar(f'Uspešna prijava kao {user_type}!', duration=2500))
				
				# Store user data in session manager
				set_current_user(user_data)
				
				# Navigate based on user type from database
				if user_data.get('is_admin', False):
					page_data.navigate('admin_dashboard')
				else:
					page_data.navigate('member_dashboard')

			else: 
				# login is not successful
				email_tf.border_color = ft.Colors.RED_300
				password_tf.border_color = ft.Colors.RED_300
				page.overlay.append(SnackBar('Greška prilikom prijave', 'Uneta je netačna e-adresa i/ili lozinka', snackbar_type='ERROR', duration=2500))
				page.update()

			
	
	email_tf = ft.TextField(
		label='E-adresa',
		prefix_icon=ft.Icons.EMAIL,
		keyboard_type=ft.KeyboardType.EMAIL,
		autofill_hints=ft.AutofillHint.EMAIL
	)
	
	# Create radio group for user type selection
	user_type_group = ft.RadioGroup(
		content=ft.Column([
			ft.Radio(value="member", label="Član biblioteke"),
			ft.Radio(value="admin", label="Administrator")
		]),
		value="member"  # Default to member
	)
	
	password_tf = ft.TextField(
		label='Lozinka',
		password=True,
		can_reveal_password=True,
		prefix_icon=ft.Icons.LOCK,
		autofill_hints=ft.AutofillHint.PASSWORD,
		on_submit=lambda _: on_submit()
	)

	container = ResponsiveForm(
		controls=[
				ft.Row(
					[ft.Text("Biblioteka - Prijava", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
					alignment=ft.MainAxisAlignment.CENTER,
				),
				ft.Row(
					[ft.Text("Izaberite tip korisnika:", size=16)],
					alignment=ft.MainAxisAlignment.CENTER,
				),
				ft.Row(
					[user_type_group],
					alignment=ft.MainAxisAlignment.CENTER,
				),
				ft.Column(
					[ 
						email_tf,
						password_tf,
					]
				),
				ft.Row(
					[
						ft.ElevatedButton(
							'Prijavi se',
							expand=True,
							height=50,
							on_click = lambda _: on_submit(),
						) 
					]
				),
				ft.Row(
					[ 
						ft.TextButton(
							'Nemaš nalog? Registruj se kao član',
							on_click=lambda _: page_data.navigate('register'),
						)
					]
				)
			]
	)

	return ft.SafeArea(container)
