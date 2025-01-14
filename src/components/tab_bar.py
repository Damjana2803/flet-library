import flet as ft 
from flet_navigator import PageData
from components.responsive_container import ResponsiveContainer

class TabBar(ResponsiveContainer): 
	def __init__(self, page_data: PageData, tab_urls = [], tab_titles = [], tab_func = [], button_height = 50, col = {'md': 6, 'lg': 4, 'xl': 3}, alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.CENTER):
		self.tab_len = len(tab_urls)
		self.tab_urls = tab_urls
		self.tab_titles = tab_titles
		self.tab_func = tab_func
		self.button_height = button_height
		self.page_data = page_data


		super().__init__(
			controls=[
				ft.Row(
					controls=self._generate_row_controls(),
					expand=True
				)
			],
			col=col,
			alignment=alignment
		)
		
	def _generate_row_controls(self):
		controls = []

		for i in range(self.tab_len):
			active = self.page_data.current_route() == self.tab_urls[i]
			controls.append(
				ft.Button(
					content=ft.Text(
						spans=[
							ft.TextSpan(
								self.tab_titles[i],
								ft.TextStyle(
									italic=active,
								)
							)
						]
					),
					height = self.button_height,
					expand = True,
					on_click = self.tab_func[i],
				)
			)

		return controls
