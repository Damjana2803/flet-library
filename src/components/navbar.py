import flet as ft
from flet_navigator import PageData
from utils.session_manager import clear_current_user

# Navigation pages for different user types
admin_pages = ['admin_dashboard', 'admin_books', 'admin_members', 'admin_loans', 'admin_statistics']
member_pages = ['member_dashboard', 'book_search', 'my_loans', 'my_reservations', 'member_profile']

def logout_user(page_data):
    """Logout user and redirect to login"""
    # Clear user data from session
    clear_current_user()
    
    # Navigate to login page
    page_data.navigate('login')

def NavBar(user_type="member", page_data=None):
    if page_data is None:
        # Return a simple navigation bar without page_data
        if user_type == "admin":
            destinations = [
                ft.NavigationBarDestination(icon=ft.Icons.DASHBOARD, label='Dashboard'),
                ft.NavigationBarDestination(icon=ft.Icons.BOOK, label='Knjige'),
                ft.NavigationBarDestination(icon=ft.Icons.PEOPLE, label='Članovi'),
                ft.NavigationBarDestination(icon=ft.Icons.LIBRARY_BOOKS, label='Pozajmica'),
                ft.NavigationBarDestination(icon=ft.Icons.ANALYTICS, label='Statistike'),
            ]
        else:  # member
            destinations = [
                ft.NavigationBarDestination(icon=ft.Icons.DASHBOARD, label='Dashboard'),
                ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label='Pretraga'),
                ft.NavigationBarDestination(icon=ft.Icons.LIBRARY_BOOKS, label='Moje knjige'),
                ft.NavigationBarDestination(icon=ft.Icons.BOOKMARK, label='Rezervacije'),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON, label='Profil'),
            ]
        
        return ft.NavigationBar(
            selected_index=0,
            destinations=destinations,
        )
    
    page = page_data.page
    current_route = page_data.current_route()
    
    if user_type == "admin":
        pages = admin_pages
        destinations = [
            ft.NavigationBarDestination(icon=ft.Icons.DASHBOARD, label='Dashboard'),
            ft.NavigationBarDestination(icon=ft.Icons.BOOK, label='Knjige'),
            ft.NavigationBarDestination(icon=ft.Icons.PEOPLE, label='Članovi'),
            ft.NavigationBarDestination(icon=ft.Icons.LIBRARY_BOOKS, label='Pozajmica'),
            ft.NavigationBarDestination(icon=ft.Icons.ANALYTICS, label='Statistike'),
        ]
    else:  # member
        pages = member_pages
        destinations = [
            ft.NavigationBarDestination(icon=ft.Icons.DASHBOARD, label='Dashboard'),
            ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label='Pretraga'),
            ft.NavigationBarDestination(icon=ft.Icons.LIBRARY_BOOKS, label='Moje knjige'),
            ft.NavigationBarDestination(icon=ft.Icons.BOOKMARK, label='Rezervacije'),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label='Profil'),
        ]
    
    # Find current page index
    if current_route in pages:
        current_index = pages.index(current_route)
    else:
        current_index = 0
    
    def handle_change(e):
        selected_index = int(e.data)
        if selected_index < len(pages):
            page_data.navigate(pages[selected_index])
    
    # Create navigation bar with logout button
    nav_bar = ft.NavigationBar(
        selected_index=current_index,
        destinations=destinations,
        on_change=lambda e: handle_change(e)
    )
    
    # Create logout button
    logout_button = ft.IconButton(
        icon=ft.Icons.LOGOUT,
        icon_color=ft.Colors.RED,
        tooltip="Odjavi se",
        on_click=lambda e: logout_user(page_data)
    )
    
    # Return both navigation bar and header with logout button
    return ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Text(
                    f"Biblioteka - {'Admin' if user_type == 'admin' else 'Član'}",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900,
                    expand=True
                ),
                logout_button
            ]),
            padding=10
        ),
        nav_bar
    ])

# Legacy function for backward compatibility
def navbar(page_data: PageData, current_page=1):
    return NavBar("member")
