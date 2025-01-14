import flet as ft

class Table(ft.ListView):
	def __init__(
		self, col_names: list[str] = [], col_keys = [],
		rows = [], row_height = 40, actions = ['EDIT', 'DELETE'],
		ignore_key = None, ignore_value=1, 
		max_characters=50, column_width = 250,
		on_edit = None, on_delete = None
	):
		self.col_names = col_names
		self.col_keys = col_keys
		self.actions = actions
		self.rows = rows
		self.ignore_value = ignore_value
		self.ignore_key = ignore_key
		self.max_characters = max_characters
		self.on_edit = on_edit
		self.on_delete = on_delete
		self.column_width = column_width
		self.row_height = row_height
		self.rows = rows
		self.head = self._generate_head()
		super().__init__(expand=True)

		self.controls = [
			ft.Container(
				ft.Row(
					scroll=ft.ScrollMode.AUTO,
					controls=[
						ft.Column(
							controls=self.head,
							alignment=ft.MainAxisAlignment.CENTER
						)
					],
					expand=True,
				),
				padding=ft.padding.symmetric(5, 10)
			)
		]

	def _generate_head(self):
		res = []

		head = ft.Row()
		for col in self.col_names:
			head.controls.append(
				ft.Column(
					[ft.Text(col, theme_style=ft.TextThemeStyle.LABEL_LARGE)],
					width = self.column_width
				)
			)

		res.append(head)
		
		for index, data in enumerate(self.rows):
			row = ft.Row(
				height=self.row_height
			)			
			for key in self.col_keys:		
				if key != 'TABLE.ACTIONS':
					if len(key) > self.max_characters:
						data[key] = data[key][:self.max_characters - 3] + '...'
					# add data to table row
					row.controls.append(
						ft.Container(
							ft.Column(

								controls=[
									ft.Text(data[key])
								],
								expand=True,
								alignment=ft.MainAxisAlignment.CENTER,
							),
							width=self.column_width
						)
					)

				else:
					action_row = ft.Row(
						controls=[],
						alignment=ft.MainAxisAlignment.START,
						expand=True,
					)
					
					if self.ignore_key is not None and data[self.ignore_key] is self.ignore_value:
						if len(action_row.controls):
							row.controls.append(ft.Column([ft.Text('')], width=self.column_width,))

					else:
						if 'EDIT' in self.actions and self.on_edit is not None:
							action_row.controls.append(
								ft.IconButton(
									icon = ft.Icons.EDIT,
									on_click = lambda _, id = index: self.on_edit(id, 'EDIT'),
								)
							)

						if 'DELETE' in self.actions and self.on_delete is not None:
							action_row.controls.append(
								ft.IconButton(
									icon = ft.Icons.DELETE,
									on_click = lambda _, id = index: self.on_delete(id, 'DELETE'),
									# style=ft.ButtonStyle(padding=ft.padding.symmetric(5, 5))
								)
							)
	
						row.controls.append(ft.Column([action_row], width=self.column_width,))

			result_row = ft.Row(
				alignment=ft.MainAxisAlignment.CENTER,
				controls=[row],
				expand=True,
			)

			res.append(
				ft.Container(
					result_row,
					border=ft.border.only(top=ft.border.BorderSide(1, "black"))
				)
			)

		return res