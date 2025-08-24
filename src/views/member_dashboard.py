import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.responsive_card import ResponsiveCard
from utils.session_manager import get_current_user
from controllers.admin_controller import get_all_books, get_member_statistics

def member_dashboard_screen(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Dashboard - Biblioteka"
    
    # Check if mobile screen
    is_mobile = page.width < 768 if page.width else False
    
    # Navigation bar
    navbar_content = NavBar("member", page_data)
    
    # Get current user data from session manager
    user = get_current_user()
    member_id = user.get('member_id') if user else None
    
    # Get comprehensive member statistics from database
    if member_id:
        member_stats = get_member_statistics(member_id)
    else:
        member_stats = {}
    
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
    
    # Create statistics cards with accurate data from database
    def create_stat_card(title, value, subtitle, color, icon=None):
        """Create a responsive statistics card"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Icon(icon, color=color, size=32) if icon else ft.Container(),
                            ft.Column([
                                ft.Text(title, size=12 if is_mobile else 14, color=ft.Colors.GREY_600),
                                ft.Text(str(value), size=20 if is_mobile else 24, weight=ft.FontWeight.BOLD, color=color),
                                ft.Text(subtitle, size=10 if is_mobile else 12, color=ft.Colors.GREY_500),
                            ], expand=True, spacing=4),
                        ], alignment=ft.MainAxisAlignment.START) if icon else ft.Column([
                            ft.Text(title, size=12 if is_mobile else 14, color=ft.Colors.GREY_600),
                            ft.Text(str(value), size=20 if is_mobile else 24, weight=ft.FontWeight.BOLD, color=color),
                            ft.Text(subtitle, size=10 if is_mobile else 12, color=ft.Colors.GREY_500),
                        ], spacing=4, alignment=ft.MainAxisAlignment.CENTER),
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=15 if is_mobile else 20,
            ),
            expand=True,
        )
    
    # Statistics cards with real data
    stats_cards = [
        create_stat_card(
            "Aktivne pozajmice",
            member_stats.get('active_loans', 0),  # Use active_loans from loans table (more accurate)
            f"od {member_stats.get('max_loans', 5)} maksimalno",
            ft.Colors.ORANGE,
            ft.Icons.LIBRARY_BOOKS
        ),
        create_stat_card(
            "Aktivne rezervacije",
            member_stats.get('active_reservations', 0),
            "trenutno rezervisano",
            ft.Colors.GREEN,
            ft.Icons.BOOKMARK
        ),
        create_stat_card(
            "Dostupne knjige",
            member_stats.get('total_available_books', 0),
            "u biblioteci",
            ft.Colors.BLUE,
            ft.Icons.MENU_BOOK
        ),
    ]
    
    # Add overdue loans card if there are any
    if member_stats.get('overdue_loans', 0) > 0:
        stats_cards.append(
            create_stat_card(
                "Zakašnjele pozajmice",
                member_stats.get('overdue_loans', 0),
                "trebaju vraćanje",
                ft.Colors.RED,
                ft.Icons.WARNING
            )
        )
    else:
        stats_cards.append(
            create_stat_card(
                "Ukupno pozajmica",
                member_stats.get('total_loans', 0),
                "svih vremena",
                ft.Colors.PURPLE,
                ft.Icons.HISTORY
            )
        )
    
    # Mobile: 2 cards per row, Desktop: all in one row or 2 rows depending on count
    if is_mobile:
        # Mobile: Create rows of 2 cards each
        stats_rows = []
        for i in range(0, len(stats_cards), 2):
            row_cards = stats_cards[i:i+2]
            if len(row_cards) == 2:
                stats_rows.append(ft.Row(row_cards, spacing=10))
            else:
                stats_rows.append(ft.Row([row_cards[0], ft.Container()], spacing=10))
        quick_stats = ft.Column(stats_rows, spacing=16)
    else:
        # Desktop: All cards in one row if 4 or less, otherwise 2 rows
        if len(stats_cards) <= 4:
            quick_stats = ft.Row(stats_cards, spacing=16)
        else:
            row1 = ft.Row(stats_cards[:3], spacing=16)
            row2 = ft.Row(stats_cards[3:], spacing=16)
            quick_stats = ft.Column([row1, row2], spacing=16)
    
    # Welcome section with member info
    welcome_section = ft.Container(
        content=ft.Column([
            ft.Text(
                f"Dobrodošli, {member_stats.get('first_name', user.get('name', 'Člane'))}!",
                size=28 if is_mobile else 32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_900,
            ),
            ft.Text(
                f"Članstvo: {member_stats.get('membership_type', 'Regular').title()} | Broj: {member_stats.get('membership_number', 'N/A')}",
                size=14 if is_mobile else 16,
                color=ft.Colors.GREY_600,
            ),
            ft.Container(
                content=ft.Text(
                    member_stats.get('membership_status', 'active').upper(),
                    size=12,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                ),
                bgcolor=ft.Colors.GREEN if member_stats.get('membership_status') == 'active' else ft.Colors.RED,
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=12,
            ) if member_stats.get('membership_status') else ft.Container(),
        ], spacing=8)
    )
    
    # Quick actions section
    quick_actions_title = ft.Text(
        "Brzi pristup",
        size=18 if is_mobile else 20,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_900,
    )
    
    # Responsive grid for action cards
    if is_mobile:
        # Mobile: 2 columns, smaller cards
        actions_grid = ft.GridView(
            runs_count=2,
            max_extent=150,
            child_aspect_ratio=1.1,
            spacing=12,
            run_spacing=12,
            controls=[search_card, loans_card, reservations_card, profile_card],
        )
    else:
        # Desktop: 4 columns, larger cards
        actions_grid = ft.GridView(
            runs_count=4,
            max_extent=200,
            child_aspect_ratio=1.0,
            spacing=16,
            run_spacing=16,
            controls=[search_card, loans_card, reservations_card, profile_card],
        )
    
    # Main scrollable content
    content = ft.Column(
        controls=[
            welcome_section,
            ft.Divider(height=20),
            quick_stats,
            ft.Divider(height=20),
            quick_actions_title,
            ft.Container(height=10),  # Small spacing
            actions_grid,
            ft.Container(height=30),  # Bottom spacing for better scrolling
        ],
        spacing=16,
        scroll=ft.ScrollMode.AUTO,  # Make the main content scrollable
        expand=True,
    )
    
    # Return the layout with proper scrolling
    return ft.Column([
        navbar_content,
        ft.Container(
            content=content,
            padding=15 if is_mobile else 20,
            expand=True,
        )
    ], expand=True)