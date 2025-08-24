import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import SnackBar
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
        # Get member data from database using member_id
        member_id = current_user.get('member_id')
        if member_id:
            from controllers.admin_controller import get_member_by_id
            current_member = get_member_by_id(member_id)
    
    # Use real member data or fallback to default
    if current_member:
        member_data = {
            "first_name": current_member.get("first_name", "Nepoznato"),
            "last_name": current_member.get("last_name", ""),
            "email": current_member.get("email", current_user.get("email", "")),
            "phone": current_member.get("phone", "N/A"),
            "address": current_member.get("address", "N/A"),
            "membership_number": current_member.get("membership_number", f"M{current_member.get('id', 'N/A')}"),
            "membership_type": current_member.get("membership_type", "regular"),
            "membership_status": current_member.get("membership_status", "active"),
            "membership_start_date": current_member.get("membership_start_date", "N/A"),
            "membership_end_date": current_member.get("membership_end_date", "N/A"),
            "current_loans": current_member.get("current_loans", 0),
            "max_loans": current_member.get("max_loans", 5)
        }
    else:
        # Fallback data using user email
        member_data = {
            "first_name": "Nepoznato",
            "last_name": "",
            "email": current_user.get("email", "nema.email@biblioteka.rs") if current_user else "nema.email@biblioteka.rs",
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
        # Create text field references
        first_name_field = ft.TextField(
            label="Ime",
            value=member_data["first_name"],
        )
        last_name_field = ft.TextField(
            label="Prezime",
            value=member_data["last_name"],
        )
        email_field = ft.TextField(
            label="E-adresa",
            value=member_data["email"],
            keyboard_type=ft.KeyboardType.EMAIL
        )
        phone_field = ft.TextField(
            label="Broj telefona",
            value=member_data["phone"],
            keyboard_type=ft.KeyboardType.PHONE
        )
        address_field = ft.TextField(
            label="Adresa",
            value=member_data["address"],
            multiline=True,
            min_lines=2,
            max_lines=3
        )
        
        def save_profile_data():
            # Get current user to access member_id
            current_user = get_current_user()
            if not current_user or not current_user.get('member_id'):
                page.overlay.append(
                    SnackBar("Greška: Korisnik nije pronađen", snackbar_type="ERROR", duration=3000)
                )
                page.update()
                return
            
            # Update member data with new values
            new_first_name = first_name_field.value
            new_last_name = last_name_field.value
            new_email = email_field.value
            new_phone = phone_field.value
            new_address = address_field.value
            
            # Save to database
            from controllers.admin_controller import update_member_profile
            success, message = update_member_profile(
                current_user['member_id'],
                new_first_name,
                new_last_name,
                new_email,
                new_phone,
                new_address
            )
            
            if success:
                page.overlay.append(
                    SnackBar("Profil je uspešno ažuriran!", duration=3000)
                )
                page.update()
                close_dialog()
                
                # Refresh the page with fresh data
                refresh_profile_data()
            else:
                page.overlay.append(
                    SnackBar(f"Greška: {message}", snackbar_type="ERROR", duration=3000)
                )
                page.update()
        
        # Show edit profile dialog
        page.dialog = ft.AlertDialog(
            title=ft.Text("Uredi profil"),
            content=ft.Column(
                [
                    first_name_field,
                    last_name_field,
                    email_field,
                    phone_field,
                    address_field,
                ],
                spacing=8,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("Otkaži", on_click=lambda _: close_dialog()),
                ft.TextButton("Sačuvaj", on_click=lambda _: save_profile_data()),
            ],
        )
        page.dialog.open = True
        page.update()
    

    
    def close_dialog():
        page.dialog.open = False
        page.update()
    
    def change_password(e):
        # Create text field references
        current_password_field = ft.TextField(
            label="Trenutna lozinka",
            password=True,
        )
        new_password_field = ft.TextField(
            label="Nova lozinka",
            password=True,
            helper_text="Najmanje 6 karaktera"
        )
        confirm_password_field = ft.TextField(
            label="Potvrdi novu lozinku",
            password=True,
        )
        
        def save_password_data():
            current_password = current_password_field.value
            new_password = new_password_field.value
            confirm_password = confirm_password_field.value
            
            # Validate inputs
            if not current_password or not new_password or not confirm_password:
                page.overlay.append(
                    SnackBar("Sva polja su obavezna!", snackbar_type="ERROR", duration=3000)
                )
                page.update()
                return
            
            if new_password != confirm_password:
                page.overlay.append(
                    SnackBar("Nova lozinka i potvrda se ne poklapaju!", snackbar_type="ERROR", duration=3000)
                )
                page.update()
                return
            
            if len(new_password) < 6:
                page.overlay.append(
                    SnackBar("Nova lozinka mora imati najmanje 6 karaktera!", snackbar_type="ERROR", duration=3000)
                )
                page.update()
                return
            
            # Get current user
            current_user = get_current_user()
            if not current_user or not current_user.get('id'):
                page.overlay.append(
                    SnackBar("Greška: Korisnik nije pronađen", snackbar_type="ERROR", duration=3000)
                )
                page.update()
                return
            
            # Hash passwords for comparison
            import hashlib
            current_password_hash = hashlib.sha256(current_password.encode()).hexdigest()
            new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            
            # Verify current password
            from controllers.admin_controller import verify_user_password
            if not verify_user_password(current_user['id'], current_password_hash):
                page.overlay.append(
                    SnackBar("Trenutna lozinka nije ispravna!", snackbar_type="ERROR", duration=3000)
                )
                page.update()
                return
            
            # Update password in database
            from controllers.admin_controller import update_user_password
            success, message = update_user_password(current_user['id'], new_password_hash)
            
            if success:
                page.overlay.append(
                    SnackBar("Lozinka je uspešno promenjena!", duration=3000)
                )
                page.update()
                close_dialog()
                
                # Refresh the page with fresh data
                refresh_profile_data()
            else:
                page.overlay.append(
                    SnackBar(f"Greška: {message}", snackbar_type="ERROR", duration=3000)
                )
                page.update()
        
        # Show change password dialog
        page.dialog = ft.AlertDialog(
            title=ft.Text("Promeni lozinku"),
            content=ft.Column(
                [
                    current_password_field,
                    new_password_field,
                    confirm_password_field,
                ],
                spacing=8,
            ),
            actions=[
                ft.TextButton("Otkaži", on_click=lambda _: close_dialog()),
                ft.TextButton("Promeni", on_click=lambda _: save_password_data()),
            ],
        )
        page.dialog.open = True
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
    
    def logout_user():
        """Logout user and clear session"""
        from utils.session_manager import clear_current_user
        clear_current_user()
        page_data.navigate('login')
    
    def refresh_profile_data():
        """Refresh profile data from database and rebuild the page"""
        nonlocal member_data
        
        # Get fresh member data from database
        current_user = get_current_user()
        if current_user and not current_user.get('is_admin', False):
            member_id = current_user.get('member_id')
            if member_id:
                from controllers.admin_controller import get_member_by_id
                fresh_member = get_member_by_id(member_id)
                if fresh_member:
                    member_data = {
                        "first_name": fresh_member.get("first_name", "Nepoznato"),
                        "last_name": fresh_member.get("last_name", ""),
                        "email": fresh_member.get("email", current_user.get("email", "")),
                        "phone": fresh_member.get("phone", "N/A"),
                        "address": fresh_member.get("address", "N/A"),
                        "membership_number": fresh_member.get("membership_number", f"M{fresh_member.get('id', 'N/A')}"),
                        "membership_type": fresh_member.get("membership_type", "regular"),
                        "membership_status": fresh_member.get("membership_status", "active"),
                        "membership_start_date": fresh_member.get("membership_start_date", "N/A"),
                        "membership_end_date": fresh_member.get("membership_end_date", "N/A"),
                        "current_loans": fresh_member.get("current_loans", 0),
                        "max_loans": fresh_member.get("max_loans", 5)
                    }
        
        # Rebuild the entire page
        page.clean()
        page.add(navbar_content)
        
        # Rebuild all components with fresh data
        fresh_profile_header = ft.Card(
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
        
        fresh_personal_info = ft.Card(
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
        
        fresh_membership_info = ft.Card(
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
        
        fresh_actions_card = ft.Card(
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
                        # ft.ListTile(
                        #     leading=ft.Icon(ft.Icons.DOWNLOAD, color=ft.Colors.GREY),
                        #     title=ft.Text("Preuzmi istoriju iznajmljivanja"),
                        #     trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, color=ft.Colors.GREY),
                        # ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED),
                            title=ft.Text("Odjavi se", color=ft.Colors.RED),
                            trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, color=ft.Colors.GREY),
                            on_click=lambda _: logout_user(),
                        ),
                    ],
                    spacing=8,
                ),
                padding=20,
            ),
        )
        
        fresh_content = ft.Column(
            controls=[
                fresh_profile_header,
                ft.Divider(height=32),
                fresh_personal_info,
                ft.Divider(height=16),
                fresh_membership_info,
                ft.Divider(height=16),
                fresh_actions_card,
                ft.Container(height=50),  # Bottom spacing
            ],
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        page.add(ft.Container(
            content=fresh_content,
            padding=20,
            expand=True,
        ))
        page.update()
    
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
                    # ft.ListTile(
                    #     leading=ft.Icon(ft.Icons.DOWNLOAD, color=ft.Colors.GREY),
                    #     title=ft.Text("Preuzmi istoriju iznajmljivanja"),
                    #     trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, color=ft.Colors.GREY),
                    # ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED),
                        title=ft.Text("Odjavi se", color=ft.Colors.RED),
                        trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, color=ft.Colors.GREY),
                        on_click=lambda _: logout_user(),
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
