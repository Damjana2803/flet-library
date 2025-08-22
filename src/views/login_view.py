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
		print("=== LOGIN ATTEMPT STARTED ===")
		print(f"Email field value: '{email_tf.value}'")
		print(f"Password field value: '{password_tf.value}'")
		print(f"User type selection: '{user_type_group.value}'")
		
		if (len(email_tf.value) != 0 and len(password_tf.value) != 0):
			print("✅ Form validation passed - fields are not empty")
			
			# Determine login type based on radio button selection
			login_type = user_type_group.value
			print(f"Selected login type: {login_type}")
			
			print("🔐 Calling login_user function...")
			success, message, user_data = login_user(email_tf.value, password_tf.value)
			
			print(f"Login result - Success: {success}")
			print(f"Login result - Message: {message}")
			print(f"Login result - User data: {user_data}")
			
			if success:
				print("✅ Login successful!")
				# login is successful
				user_type = "Administrator" if user_data.get('is_admin', False) else "Član"
				print(f"User type for display: {user_type}")
				print(f"Is admin flag: {user_data.get('is_admin', False)}")
				
				page.overlay.append(SnackBar(f'Uspešna prijava kao {user_type}!', duration=2500))
				print("✅ Success snackbar added")
				
				# Store user data in session manager
				print("💾 Setting current user in session manager...")
				set_current_user(user_data)
				print("✅ User data stored in session")
				
				# Navigate based on user type from database
				if user_data.get('is_admin', False):
					print("🚀 Navigating to admin_dashboard...")
					page_data.navigate('admin_dashboard')
				else:
					print("🚀 Navigating to member_dashboard...")
					page_data.navigate('member_dashboard')
				
				print("✅ Navigation completed")

			else: 
				print("❌ Login failed!")
				# login is not successful
				email_tf.border_color = ft.Colors.RED_300
				password_tf.border_color = ft.Colors.RED_300
				page.overlay.append(SnackBar('Greška prilikom prijave', 'Uneta je netačna e-adresa i/ili lozinka', snackbar_type='ERROR', duration=2500))
				page.update()
				print("❌ Error snackbar added and page updated")

		else:
			print("❌ Form validation failed - empty fields detected")
			print(f"Email length: {len(email_tf.value)}")
			print(f"Password length: {len(password_tf.value)}")
	
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
