import flet as ft, asyncio

class RateModal(ft.AlertDialog):
	def __init__(self, title: str, page: ft.Page, on_save = None, on_close = None, **kwargs):
		self.title = title
		self.page = page
		self.rating = 0
		self.on_save = on_save
		self.on_close = on_close

		self.icons = ft.Row(controls=self._init_stars())
		self.tf = ft.TextField(label='Komentar', max_lines=5)
		
		super().__init__(
			modal=True,
			title=ft.Text(self.title),
			content=ft.Container(
				height=200,
				content=ft.Column(
					scroll=ft.ScrollMode.HIDDEN,
					controls=[
						self.icons,
						self.tf
					]
				)
			),
			actions=[
				ft.TextButton('Odbaci', on_click=self.on_close),
				ft.TextButton('Sačuvaj', on_click=lambda _: self.handle_save())
			],
			**kwargs
		)

	def _init_stars(self):
		unrated = 5 - self.rating
		controls = []
		
		for i in range(self.rating):
			controls.append(
				ft.Container(
					content=ft.IconButton(icon=ft.Icons.STAR, on_click=lambda _, index = i: self._handle_rating(index + 1)),
					on_hover=lambda e, index = i + self.rating: self._handle_hover(e, index)
				)
			)

		for i in range(unrated):
			controls.append(
				ft.Container(
					content=ft.IconButton(
						icon=ft.Icons.STAR_BORDER,
						on_click=lambda _, index = i + self.rating: self._handle_rating(index + 1)
					),
					on_hover=lambda e, index = i + self.rating: self._handle_hover(e, index)
				)
				
			)

		return controls

	def _handle_rating(self, index):
		self.rating = index
		self.icons.controls = self._init_stars()
		self.page.update() 

	def _handle_hover(self, e, index):
		if self.rating == 0:
			for i in range(index + 1):
				self.icons.controls[i].content.icon = ft.Icons.STAR if e.data == 'true' else ft.Icons.STAR_BORDER
				self.icons.controls[i].update()

	def handle_save(self):
		asyncio.run(self.on_save(self.rating, self.tf.value))
		self.on_close()
