import flet as ft

class ResponsiveContainer(ft.ResponsiveRow):
	def __init__(self, controls = [], col = {'md': 6, 'lg': 4, 'xl': 3}, alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.CENTER, **kwargs):
		super().__init__(
			alignment=alignment,
			controls=[
				ft.Column(
					col=col,
					controls=[
						ft.Row(
							controls=controls
						)
					]
				)
			],
			**kwargs
		)
		