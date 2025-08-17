import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.responsive_card import ResponsiveCard
from components.snack_bar import SnackBar
from utils.global_state import global_state

def admin_dashboard(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Admin Dashboard - Biblioteka"
    
    # Navigation bar
    navbar_content = NavBar("admin", page_data)
    
    def navigate_to_books(e):
        page_data.navigate('admin_books')
    
    def navigate_to_members(e):
        page_data.navigate('admin_members')
    
    def navigate_to_loans(e):
        page_data.navigate('admin_loans')
    
    def navigate_to_statistics(e):
        page_data.navigate('admin_statistics')
    
    # Dashboard cards
    books_card = ResponsiveCard(
        title="Upravljanje knjigama",
        subtitle="Dodaj, uređuj i upravljaj bibliotečkim fondom",
        icon=ft.Icons.BOOK,
        color=ft.Colors.BLUE,
        on_click=navigate_to_books
    )
    
    members_card = ResponsiveCard(
        title="Upravljanje članovima",
        subtitle="Registruj članove i upravljaj članarinama",
        icon=ft.Icons.PEOPLE,
        color=ft.Colors.GREEN,
        on_click=navigate_to_members
    )
    
    loans_card = ResponsiveCard(
        title="Iznajmljivanje",
        subtitle="Prati iznajmljene knjige i vraćanja",
        icon=ft.Icons.LIBRARY_BOOKS,
        color=ft.Colors.ORANGE,
        on_click=navigate_to_loans
    )
    
    statistics_card = ResponsiveCard(
        title="Statistike",
        subtitle="Pregled najtraženijih knjiga i evidencija",
        icon=ft.Icons.ANALYTICS,
        color=ft.Colors.PURPLE,
        on_click=navigate_to_statistics
    )
    
    # Get real data from global state
    books = global_state.get("books", [])
    members = global_state.get("members", [])
    loans = global_state.get("loans", [])
    
    # Calculate statistics
    total_books = len(books)
    total_members = len(members)
    active_loans = len([loan for loan in loans if loan['status'] == 'active'])

    available_books = len([book for book in books if book['available_copies'] > 0])
    
    # Quick stats row
    quick_stats = ft.Row(
        [
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Ukupno knjiga", size=14, color=ft.Colors.GREY_600),
                            ft.Text(str(total_books), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                            ft.Text(f"Dostupno: {available_books}", size=12, color=ft.Colors.GREY_500),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=20,
                ),
                expand=True,
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Aktivnih članova", size=14, color=ft.Colors.GREY_600),
                            ft.Text(str(total_members), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
                            ft.Text(f"Tip: {len([m for m in members if m['membership_type'] == 'student'])} studenata", size=12, color=ft.Colors.GREY_500),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=20,
                ),
                expand=True,
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Aktivne pozajmice", size=14, color=ft.Colors.GREY_600),
                            ft.Text(str(active_loans), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE),

                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=20,
                ),
                expand=True,
            ),
        ],
        spacing=16,
    )
    
    # Main content using ListView for proper scrolling
    content = ft.ListView(
        controls=[
            ft.Text(
                "Admin Dashboard",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_900,
            ),
            ft.Text(
                "Dobrodošli u sistem upravljanja bibliotekom",
                size=16,
                color=ft.Colors.GREY_600,
            ),
            ft.Divider(height=32),
            quick_stats,
            ft.Divider(height=32),
            ft.Text(
                "Detaljni pregled",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_900,
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Knjige", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ft.Row([
                            ft.Text(f"• Ukupno: {total_books} knjiga", size=14),
                            ft.Text(f"• Dostupno: {available_books} knjiga", size=14, color=ft.Colors.GREEN),
                            ft.Text(f"• Nedostupno: {total_books - available_books} knjiga", size=14, color=ft.Colors.RED),
                        ], wrap=True),
                        ft.Divider(height=16),
                        ft.Text("Članovi", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ft.Row([
                            ft.Text(f"• Ukupno: {total_members} članova", size=14),
                            ft.Text(f"• Studenata: {len([m for m in members if m['membership_type'] == 'student'])}", size=14),
                            ft.Text(f"• Redovnih: {len([m for m in members if m['membership_type'] == 'regular'])}", size=14),
                            ft.Text(f"• Penzionera: {len([m for m in members if m['membership_type'] == 'senior'])}", size=14),
                        ], wrap=True),
                        ft.Divider(height=16),
                        ft.Text("Pozajmice", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ft.Row([
                            ft.Text(f"• Aktivne: {active_loans} pozajmica", size=14, color=ft.Colors.ORANGE),
                            ft.Text(f"• Vraćene: {len([loan for loan in loans if loan['status'] == 'returned'])} pozajmica", size=14, color=ft.Colors.GREEN),
                        ], wrap=True),
                    ]),
                    padding=20,
                ),
            ),
            ft.Divider(height=32),
            ft.Text(
                "Brzi pristup",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_900,
            ),
            ft.GridView(
                runs_count=2,
                max_extent=200,
                child_aspect_ratio=1.0,
                spacing=16,
                run_spacing=16,
                controls=[
                    books_card,
                    members_card,
                    loans_card,
                    statistics_card,
                ],
            ),
            ft.Container(height=50),  # Bottom spacing
        ],
        spacing=16,
        expand=True,
    )
    
    return ft.Column([
        navbar_content,
        ft.Container(
            content=content,
            padding=20,
            expand=True,

        )
    ])
