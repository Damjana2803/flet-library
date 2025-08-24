import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import show_snack_bar
from utils.session_manager import get_current_user

def member_profile(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Moj profil - Biblioteka"
    
    # Check if mobile screen
    page_width = page.width if page.width else 1200
    is_mobile = page_width < 768
    
    # Navigation bar
    navbar_content = NavBar("member", page_data)
    
    # Get current logged-in member data from session manager
    current_user = get_current_user()
    current_member = None
    
    if current_user and not current_user.get('is_admin', False):
        # For member users, the login_data already contains member information
        current_member = current_user
    elif current_user:
        # Fallback: search by email in members list from database
        current_user_email = current_user.get('email')
        if current_user_email:
            from controllers.admin_controller import get_all_members
            all_members = get_all_members()
            for member in all_members:
                if member.get('email') == current_user_email:
                    current_member = member
                    break
    
    # Use real member data or fallback to default
    if current_member:
        member_data = {
            "first_name": current_member.get("first_name", "Nepoznato"),
            "last_name": current_member.get("last_name", ""),
            "email": current_member.get("email", ""),
            "phone": current_member.get("phone", ""),
            "address": current_member.get("address", ""),
            "membership_number": current_member.get("membership_number", ""),
            "membership_type": current_member.get("membership_type", "regular"),
            "membership_status": current_member.get("membership_status", "active"),
            "membership_start_date": current_member.get("membership_start_date", ""),
            "membership_end_date": current_member.get("membership_end_date", ""),
            "current_loans": current_member.get("current_loans", 0),
            "max_loans": current_member.get("max_loans", 5)
        }
    else:
        # Fallback data
        member_data = {
            "first_name": "Nepoznato",
            "last_name": "",
            "email": "nema.email@biblioteka.rs",
            "phone": "N/A",
            "address": "N/A",
            "membership_number": "N/A",
            "membership_type": "regular",
            "membership_status": "active",
            "membership_start_date": "N/A",
            "membership_end_date": "N/A",
            "current_loans": 0,
            "max_loans": 5
        }
    
    def edit_profile(e):
        # Show edit profile dialog
        page.dialog = ft.AlertDialog(
            title=ft.Text("Uredi profil"),
            content=ft.Column(
                [
                    ft.TextField(
                        label="Ime",
                        value=member_data["first_name"],
                        id="first_name"
                    ),
                    ft.TextField(
                        label="Prezime",
                        value=member_data["last_name"],
                        id="last_name"
                    ),
                    ft.TextField(
                        label="E-adresa",
                        value=member_data["email"],
                        id="email",
                        keyboard_type=ft.KeyboardType.EMAIL
                    ),
                    ft.TextField(
                        label="Broj telefona",
                        value=member_data["phone"],
                        id="phone",
                        keyboard_type=ft.KeyboardType.PHONE
                    ),
                    ft.TextField(
                        label="Adresa",
                        value=member_data["address"],
                        id="address",
                        multiline=True,
                        min_lines=2,
                        max_lines=3
                    ),
                ],
                spacing=8,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("Otkaži", on_click=lambda _: close_dialog()),
                ft.TextButton("Sačuvaj", on_click=lambda _: save_profile()),
            ],
        )
        page.dialog.open = True
        page.update()
    
    def save_profile():
        # In a real app, this would save to database
        show_snack_bar(page, "Profil je uspešno ažuriran!", "SUCCESS")
        close_dialog()
        page.update()
    
    def close_dialog():
        page.dialog.open = False
        page.update()
    
    def change_password(e):
        # Show change password dialog
        page.dialog = ft.AlertDialog(
            title=ft.Text("Promeni lozinku"),
            content=ft.Column(
                [
                    ft.TextField(
                        label="Trenutna lozinka",
                        password=True,
                        id="current_password"
                    ),
                    ft.TextField(
                        label="Nova lozinka",
                        password=True,
                        id="new_password",
                        helper_text="Najmanje 6 karaktera"
                    ),
                    ft.TextField(
                        label="Potvrdi novu lozinku",
                        password=True,
                        id="confirm_password"
                    ),
                ],
                spacing=8,
            ),
            actions=[
                ft.TextButton("Otkaži", on_click=lambda _: close_dialog()),
                ft.TextButton("Promeni", on_click=lambda _: save_password()),
            ],
        )
        page.dialog.open = True
        page.update()
    
    def save_password():
        # In a real app, this would validate and save password
        show_snack_bar(page, "Lozinka je uspešno promenjena!", "SUCCESS")
        close_dialog()
        page.update()
    
    def get_membership_type_text(membership_type):
        types = {
            "regular": "Redovno članstvo",
            "student": "Studentsko članstvo",
            "senior": "Penzionersko članstvo"
        }
        return types.get(membership_type, membership_type)
    
    def get_status_color(status):
        if status == "active":
            return ft.Colors.GREEN
        elif status == "suspended":
            return ft.Colors.RED
        else:
            return ft.Colors.GREY
    
    # Profile header
    profile_header = ft.Card(
        content=ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.PERSON, size=60, color=ft.Colors.BLUE),
                    ft.Column(
                        [
                            ft.Text(
                                f"{member_data['first_name']} {member_data['last_name']}",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                f"Član broj: {member_data['membership_number']}",
                                size=16,
                                color=ft.Colors.GREY_600,
                            ),
                            ft.Text(
                                f"Status: {member_data['membership_status'].title()}",
                                size=14,
                                color=get_status_color(member_data['membership_status']),
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=8,
                    ),
                ],
                spacing=20,
            ),
            padding=20,
        ),
    )
    
    # Personal information
    personal_info = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Lični podaci",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_900,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                on_click=edit_profile,
                                tooltip="Uredi profil",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(height=16),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.EMAIL, color=ft.Colors.GREY),
                        title=ft.Text("E-adresa"),
                        subtitle=ft.Text(member_data["email"]),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PHONE, color=ft.Colors.GREY),
                        title=ft.Text("Broj telefona"),
                        subtitle=ft.Text(member_data["phone"]),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.GREY),
                        title=ft.Text("Adresa"),
                        subtitle=ft.Text(member_data["address"]),
                    ),
                ],
                spacing=8,
            ),
            padding=20,
        ),
    )
    
    # Membership information
    membership_info = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Informacije o članstvu",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),
                    ft.Divider(height=16),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CARD_MEMBERSHIP, color=ft.Colors.GREY),
                        title=ft.Text("Tip članstva"),
                        subtitle=ft.Text(get_membership_type_text(member_data["membership_type"])),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CALENDAR_TODAY, color=ft.Colors.GREY),
                        title=ft.Text("Datum početka"),
                        subtitle=ft.Text(member_data["membership_start_date"]),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.GREY),
                        title=ft.Text("Datum isteka"),
                        subtitle=ft.Text(member_data["membership_end_date"]),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LIBRARY_BOOKS, color=ft.Colors.GREY),
                        title=ft.Text("Iznajmljene knjige"),
                        subtitle=ft.Text(f"{member_data['current_loans']} od {member_data['max_loans']}"),
                    ),
                ],
                spacing=8,
            ),
            padding=20,
        ),
    )
    
    # Actions
    actions_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Akcije",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),
                    ft.Divider(height=16),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LOCK, color=ft.Colors.GREY),
                        title=ft.Text("Promeni lozinku"),
                        trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, color=ft.Colors.GREY),
                        on_click=change_password,
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.DOWNLOAD, color=ft.Colors.GREY),
                        title=ft.Text("Preuzmi istoriju iznajmljivanja"),
                        trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, color=ft.Colors.GREY),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED),
                        title=ft.Text("Odjavi se", color=ft.Colors.RED),
                        trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, color=ft.Colors.GREY),
                        on_click=lambda _: page_data.navigate_homepage(),
                    ),
                ],
                spacing=8,
            ),
            padding=20,
        ),
    )
    
    # Main content with Column for proper scrolling
    content = ft.Column(
        controls=[
            profile_header,
            ft.Divider(height=32),
            personal_info,
            ft.Divider(height=16),
            membership_info,
            ft.Divider(height=16),
            actions_card,
            ft.Container(height=50),  # Bottom spacing
        ],
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    
    return ft.Column([
        navbar_content,
        ft.Container(
            content=content,
            padding=20,
            expand=True,
        )
    ], expand=True)
