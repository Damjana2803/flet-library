import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.responsive_card import ResponsiveCard
from components.snack_bar import SnackBar

def member_dashboard(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Član Dashboard - Biblioteka"
    
    # Navigation bar
    navbar_content = NavBar("member", page_data)
    
    def navigate_to_search(e):
        page_data.navigate('book_search')
    
    def navigate_to_my_loans(e):
        page_data.navigate('my_loans')
    
    def navigate_to_reservations(e):
        page_data.navigate('my_reservations')
    
    def navigate_to_profile(e):
        page_data.navigate('member_profile')
    
    # Dashboard cards
    search_card = ResponsiveCard(
        title="Pretraga knjiga",
        subtitle="Pronađi knjige u bibliotečkom fondu",
        icon=ft.Icons.SEARCH,
        color=ft.Colors.BLUE,
        on_click=navigate_to_search
    )
    
    my_loans_card = ResponsiveCard(
        title="Moje iznajmljene knjige",
        subtitle="Pregled trenutno iznajmljenih knjiga",
        icon=ft.Icons.LIBRARY_BOOKS,
        color=ft.Colors.GREEN,
        on_click=navigate_to_my_loans
    )
    
    reservations_card = ResponsiveCard(
        title="Moje rezervacije",
        subtitle="Upravljaj rezervacijama knjiga",
        icon=ft.Icons.BOOKMARK,
        color=ft.Colors.ORANGE,
        on_click=navigate_to_reservations
    )
    
    profile_card = ResponsiveCard(
        title="Moj profil",
        subtitle="Pregled i uređivanje podataka",
        icon=ft.Icons.PERSON,
        color=ft.Colors.PURPLE,
        on_click=navigate_to_profile
    )
    
    # Get current user data
    from utils.global_state import global_state
    current_user = global_state.get("user", {})
    
    # Member info card
    member_info = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.PERSON, size=40, color=ft.Colors.BLUE),
                            ft.Column(
                                [
                                    ft.Text(f"{current_user.get('first_name', '')} {current_user.get('last_name', '')}", size=20, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Član broj: {current_user.get('membership_number', '')}", size=14, color=ft.Colors.GREY_600),
                                    ft.Text(f"Status: {current_user.get('membership_status', '')}", size=14, color=ft.Colors.GREEN),
                                ],
                                spacing=4,
                            ),
                        ],
                        spacing=16,
                    ),
                    ft.Divider(height=16),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("Iznajmljeno", size=14, color=ft.Colors.GREY_600),
                                    ft.Text(str(current_user.get('current_loans', 0)), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                expand=True,
                            ),
                            ft.Column(
                                [
                                    ft.Text("Maksimalno", size=14, color=ft.Colors.GREY_600),
                                    ft.Text(str(current_user.get('max_loans', 5)), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                expand=True,
                            ),
                        ],
                        spacing=16,
                    ),
                ],
                spacing=16,
            ),
            padding=20,
        ),
    )
    
    # Get user's recent loans
    all_loans = global_state.get("loans", [])
    user_loans = [loan for loan in all_loans if loan.get("member_id") == current_user.get("id")]
    recent_loans = user_loans[:3]  # Show last 3 loans
    
    # Recent activity
    activity_items = [
        ft.Text("Nedavna aktivnost", size=18, weight=ft.FontWeight.BOLD),
        ft.Divider(height=16),
    ]
    
    if recent_loans:
        for loan in recent_loans:
            activity_items.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LIBRARY_BOOKS, color=ft.Colors.BLUE),
                    title=ft.Text(f"Iznajmljena knjiga: '{loan.get('book_title', '')}'"),
                    subtitle=ft.Text(f"Datum: {loan.get('loan_date', '')}"),
                    trailing=ft.Text(f"Status: {loan.get('status', '')}", size=12, color=ft.Colors.GREY_600),
                )
            )
    else:
        activity_items.append(
            ft.Text(
                "Nemate nedavnih aktivnosti",
                size=14,
                color=ft.Colors.GREY_600,
                text_align=ft.TextAlign.CENTER,
            )
        )
    
    recent_activity = ft.Card(
        content=ft.Container(
            content=ft.Column(activity_items, spacing=8),
            padding=20,
        ),
    )
    
    # Main content
    content = ft.Column(
        [
            ft.Text(
                "Dobrodošli u biblioteku",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_900,
            ),
            ft.Text(
                "Vaš lični prostor za upravljanje knjigama",
                size=16,
                color=ft.Colors.GREY_600,
            ),
            ft.Divider(height=32),
            member_info,
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
                    my_loans_card,
                    reservations_card,
                    profile_card,
                ],
            ),
            ft.Divider(height=32),
            recent_activity,
        ],
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
    )
    
    return ft.Column([
        navbar_content,
        ft.Container(
            content=content,
            padding=20,
            expand=True,

        )
    ])
