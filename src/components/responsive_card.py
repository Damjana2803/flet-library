import flet as ft

class ResponsiveForm(ft.Container):
	def __init__(self, controls, col = {'md': 6, 'lg': 5, 'xl': 4}, alignment = ft.MainAxisAlignment.CENTER):
		super().__init__(
			ft.ResponsiveRow(
				[
					ft.Column(
						col=col,
						controls=controls,
					)
				],
				alignment=alignment
			)
		)

class ResponsiveCard(ft.GestureDetector):
    def __init__(self, title="", subtitle="", icon=ft.Icons.INFO, color=ft.Colors.BLUE, on_click=None):
        card_content = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(
                            icon,
                            size=40,
                            color=color,
                        ),
                        ft.Text(
                            title,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            subtitle,
                            size=12,
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    spacing=12,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
                alignment=ft.alignment.center,
            ),
        )
        
        super().__init__(
            content=card_content,
            on_tap=on_click,
        )