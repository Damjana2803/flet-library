import flet as ft 

class Table(ft.ListView):
	def __init__(self, col_names: list[str] = [], col_keys = [], rows = [], row_height = 40, actions = ['EDIT', 'DELETE'], ignore_key = 'is_admin', ignore_value=True, max_characters=50, on_edit = None, on_delete = None):
		self.col_names = col_names
		self.col_keys = col_keys
		self.actions = actions
		self.rows = rows
		self.ignore_value = ignore_value
		self.ignore_key = ignore_key
		self.max_characters = max_characters
		self.on_edit = on_edit
		self.on_delete = on_delete
		self.row_height = row_height

		self.fake_data = [
    {
        "id": 1,  # Sequential ID
        "email": "john.doe@example.com",
        "name": "John Doe",
        "faculty": "Computer Science",
        'is_admin': True
    },
    {
        "id": 2,  # Sequential ID
        "email": "jane.smith@example.com",
        "name": "Jane Smith",
        "faculty": "Engineering",
        'is_admin': False
    },
    {
        "id": 3,  # Sequential ID
        "email": "alice.johnson@example.com",
        "name": "Alice Johnson",
        "faculty": "Mathematics",
        'is_admin': False
    },
    {
        "id": 4,  # Sequential ID
        "email": "bob.brown@example.com",
        "name": "Bob Brown",
        "faculty": "Biology",
        'is_admin': False
    },
    {
        "id": 5,  # Sequential ID
        "email": "charlie.miller@example.com",
        "name": "Charlie Miller",
        "faculty": "Physics",
        'is_admin': False
    },
    {
        "id": 6,  # Sequential ID
        "email": "emily.davis@example.com",
        "name": "Emily Davis",
        "faculty": "Chemistry",
        'is_admin': False
    },
    {
        "id": 7,  # Sequential ID
        "email": "david.wilson@example.com",
        "name": "David Wilson",
        "faculty": "Literature",
        'is_admin': False
    },
    {
        "id": 8,  # Sequential ID
        "email": "laura.moore@example.com",
        "name": "Laura Moore",
        "faculty": "History",
        'is_admin': False
    },
    {
        "id": 9,  # Sequential ID
        "email": "michael.taylor@example.com",
        "name": "Michael Taylor",
        "faculty": "Law",
        'is_admin': False
    },
    {
        "id": 10,  # Sequential ID
        "email": "susan.lee@example.com",
        "name": "Susan Lee",
        "faculty": "Art & Design",
        'is_admin': False
    }
]

		self.head = self._generate_head()
		super().__init__(expand=True)

		self.controls = [
			ft.Row(
				alignment=ft.MainAxisAlignment.SPACE_AROUND,
				vertical_alignment=ft.CrossAxisAlignment.START,
				scroll=ft.ScrollMode.AUTO,
				controls=self.head,
				expand=True 
			)
		]

	def _generate_head(self):
		res = []

		for index, col in enumerate(self.col_names):
			controls = [
				ft.Text(
					col,
					height=self.row_height,
					theme_style=ft.TextThemeStyle.LABEL_LARGE,
					text_align=ft.TextAlign.CENTER
				),
			]

			for data in self.fake_data:
				key = self.col_keys[index]

				
				if key != 'TABLE.ACTIONS':

					if len(data[key]) > self.max_characters:
						data[key] = data[key][:self.max_characters - 3] + '...'
					# add data to table row
					controls.append(
						ft.Text(data[key], height=self.row_height) 
					)

				else:
					if data[self.ignore_key] is not self.ignore_value:
						row = ft.Row(
							height=self.row_height,
							spacing=10,
							alignment=ft.MainAxisAlignment.CENTER,  # Center the buttons horizontally
							vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Center the buttons vertically
							expand=True,
						)
						
						if 'EDIT' in self.actions and self.on_edit is not None:
							row.controls.append(
								ft.IconButton(
									height=self.row_height,
									icon = ft.Icons.EDIT,
									on_click = lambda _, id = data['id']: self.on_edit(id, 'EDIT'),
								)
							)

						if 'DELETE' in self.actions and self.on_delete is not None:
							row.controls.append(
								ft.IconButton(
									height=self.row_height,
									icon = ft.Icons.DELETE,
									on_click = lambda _, id = data['id']: self.on_delete(id, 'DELETE'),
									# style=ft.ButtonStyle(padding=ft.padding.symmetric(5, 5))
								)
							)

						if len(row.controls):
							controls.append(row)
					
					else:
						controls.append(ft.Text('', height=self.row_height))

			res.append(
				ft.Column(
					spacing=10,
					alignment=ft.MainAxisAlignment.CENTER,
					horizontal_alignment=ft.CrossAxisAlignment.START,
					controls=controls,
					expand=True 
				)
			)

		return res

