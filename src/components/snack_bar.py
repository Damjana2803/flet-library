import flet as ft

class SnackBarTypes:
	SUCCESS = 'SUCCESS'
	ERROR = 'ERROR'
	INFO = 'INFO'

bgcolors = {
	'SUCCESS': ft.Colors.GREEN_100,
	'ERROR': ft.Colors.RED_100,
	'INFO': ft.Colors.WHITE60,
	'error': ft.Colors.RED_100,
	'success': ft.Colors.GREEN_100,
	'info': ft.Colors.WHITE60,
}

class SnackBar(ft.SnackBar):
	def __init__(self, title: str, subtitle: str | None = None, duration = 4000, snackbar_type: SnackBarTypes | str = SnackBarTypes.SUCCESS, open = True):
		self.column = ft.Column([
			ft.Text(title, weight=ft.FontWeight.BOLD),
		])
		super().__init__(self.column)
		self.snackbar_type = snackbar_type
		
		self.open = open
		self.duration = duration
		self.bgcolor = bgcolors[snackbar_type]
		self.content = self.column

		if subtitle is not None:
			self.column.controls.append(ft.Text(subtitle))
					
	def append_error(self, error: str):
		if self.snackbar_type == SnackBarTypes.ERROR:
			self.column.controls.append(ft.Text(f'• {error}'))

def show_snack_bar(page: ft.Page, message: str, snackbar_type: str = SnackBarTypes.SUCCESS, duration: int = 4000):
	"""
	Prikazuje snack bar sa porukom
	
	Args:
		page: Flet page objekat
		message: Poruka za prikaz
		snackbar_type: Tip snack bara ('SUCCESS', 'ERROR', 'INFO')
		duration: Trajanje u milisekundama
	"""
	snack_bar = SnackBar(
		title=message,
		snackbar_type=snackbar_type,
		duration=duration
	)
	page.show_snack_bar(snack_bar)



