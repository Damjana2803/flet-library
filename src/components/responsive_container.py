import flet as ft

class ResponsiveContainer(ft.ResponsiveRow):
	def __init__(self, controls, col = {'md': 6, 'lg': 4, 'xl': 3}, alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.CENTER):
		super().__init__()
		
		self.controls.append(
			ft.Column(
				col=col,
				controls=[
					ft.Row(
						controls=controls
					)
				]
			)
		),

		self.alignment = alignment
		