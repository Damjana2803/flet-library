import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.responsive_card import ResponsiveCard
from utils.session_manager import get_current_user
from controllers.admin_controller import get_all_books

def member_dashboard_screen(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Dashboard - Biblioteka"
    
    # Check if mobile screen
    is_mobile = page.width < 768 if page.width else False
    
    # Navigation bar
    navbar_content = NavBar("member", page_data)
    
    # Get current user data from session manager
    user = get_current_user()
    
    def navigate_to_search(e):
        page_data.navigate('book_search')
    
    def navigate_to_loans(e):
        page_data.navigate('my_loans')
    
    def navigate_to_reservations(e):
        page_data.navigate('my_reservations')
    
    def navigate_to_profile(e):
        page_data.navigate('member_profile')
    
    # Dashboard cards using ResponsiveCard like admin
    search_card = ResponsiveCard(
        title="Pretraži knjige",
        subtitle="Pronađi i rezerviši knjige",
        icon=ft.Icons.SEARCH,
        color=ft.Colors.BLUE,
        on_click=navigate_to_search
    )
    
    loans_card = ResponsiveCard(
        title="Moje pozajmice",
        subtitle="Pregled aktivnih pozajmica",
        icon=ft.Icons.LIBRARY_BOOKS,
        color=ft.Colors.ORANGE,
        on_click=navigate_to_loans
    )
    
    reservations_card = ResponsiveCard(
        title="Moje rezervacije",
        subtitle="Upravljaj rezervacijama",
        icon=ft.Icons.BOOKMARK,
        color=ft.Colors.GREEN,
        on_click=navigate_to_reservations
    )
    
    profile_card = ResponsiveCard(
        title="Moj profil",
        subtitle="Podešavanja naloga",
        icon=ft.Icons.PERSON,
        color=ft.Colors.PURPLE,
        on_click=navigate_to_profile
    )
    
    # Get real data from database
    books = get_all_books()
    available_books = len([book for book in books if book.get('available_copies', 0) > 0])
    
    # Quick stats row
    # Stats cards 
    stats_cards = [
        ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Aktivne pozajmice", size=14, color=ft.Colors.GREY_600),
                        ft.Text(str(user.get('current_loans', 0)), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE),
                        ft.Text(f"od {user.get('max_loans', 5)} maksimalno", size=12, color=ft.Colors.GREY_500),
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
                        ft.Text("Dostupno knjiga", size=14, color=ft.Colors.GREY_600),
                        ft.Text(str(available_books), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                        ft.Text("u biblioteci", size=12, color=ft.Colors.GREY_500),
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
                        ft.Text("Tip članstva", size=14, color=ft.Colors.GREY_600),
                        ft.Text(user.get('membership_type', 'Regular').title(), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
                        ft.Text(user.get('membership_number', 'N/A'), size=12, color=ft.Colors.GREY_500),
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=20,
            ),
            expand=True,
        ),
    ]
    
    # Mobile: stack cards vertically, Desktop: horizontal row
    if is_mobile:
        quick_stats = ft.Column(stats_cards, spacing=16)
    else:
        quick_stats = ft.Row(stats_cards, spacing=16)
    
    # Main content using ListView for proper scrolling
    content = ft.ListView(
        controls=[
            ft.Text(
                f"Dobrodošli, {user.get('first_name', 'Člane')}!",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_900,
            ),
            ft.Text(
                "Vaš lični dashboard biblioteke",
                size=16,
                color=ft.Colors.GREY_600,
            ),
            ft.Divider(height=32),
            quick_stats,
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
                    search_card,
                    loans_card,
                    reservations_card,
                    profile_card,
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