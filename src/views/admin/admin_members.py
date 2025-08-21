import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import show_snack_bar
from models.member import Member
from controllers.admin_controller import get_all_members, add_member, update_member, delete_member
from datetime import datetime

def admin_members(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Biblioteka | Upravljanje članovima"
    navbar_content = NavBar("admin", page_data)
    
    # Get members from database
    members_data = get_all_members()
    
    # If no members exist, initialize with sample data
    if not members_data:
        # Add sample members using the database function
        sample_members = [
            {
                "first_name": "Ana",
                "last_name": "Petrović",
                "email": "ana.petrovic@email.com",
                "phone": "+381 11 123 4567",
                "address": "Beograd, Srbija",
                "membership_number": "MEM001",
                "membership_type": "regular"
            },
            {
                "first_name": "Marko",
                "last_name": "Jovanović",
                "email": "marko.jovanovic@email.com",
                "phone": "+381 11 234 5678",
                "address": "Novi Sad, Srbija",
                "membership_number": "MEM002",
                "membership_type": "student"
            },
            {
                "first_name": "Jelena",
                "last_name": "Nikolić",
                "email": "jelena.nikolic@email.com",
                "phone": "+381 11 345 6789",
                "address": "Niš, Srbija",
                "membership_number": "MEM003",
                "membership_type": "senior"
            }
        ]
        
        for member in sample_members:
            add_member(**member)
        
        # Reload members after adding sample data
        members_data = get_all_members()
    
    # Check if mobile screen
    is_mobile = page.width < 768 if page.width else False
    
    # Dialog fields for adding new member
    first_name_field = ft.TextField(
        hint_text="Ana",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(first_name_field, "Ime je obavezno")
    )
    last_name_field = ft.TextField(
        hint_text="Petrović",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(last_name_field, "Prezime je obavezno")
    )
    email_field = ft.TextField(
        hint_text="ana.petrovic@email.com",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(email_field, "Email je obavezan")
    )
    phone_field = ft.TextField(
        hint_text="+381 11 123 4567",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400)
    )
    address_field = ft.TextField(
        hint_text="Beograd, Srbija",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400)
    )
    membership_type_field = ft.Dropdown(
        hint_text="Izaberite tip članstva",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        options=[
            ft.dropdown.Option("regular", "Redovno"),
            ft.dropdown.Option("student", "Studentsko"),
            ft.dropdown.Option("senior", "Penzionersko")
        ]
    )
    membership_status_field = ft.Dropdown(
        hint_text="Izaberite status",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        options=[
            ft.dropdown.Option("active", "Aktivno"),
            ft.dropdown.Option("suspended", "Suspendovano"),
            ft.dropdown.Option("expired", "Isteklo")
        ]
    )
    
    # Edit member dialog fields
    edit_first_name_field = ft.TextField(
        hint_text="Ana",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(edit_first_name_field, "Ime je obavezno")
    )
    edit_last_name_field = ft.TextField(
        hint_text="Petrović",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(edit_last_name_field, "Prezime je obavezno")
    )
    edit_email_field = ft.TextField(
        hint_text="ana.petrovic@email.com",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(edit_email_field, "Email je obavezan")
    )
    edit_phone_field = ft.TextField(
        hint_text="+381 11 123 4567",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400)
    )
    edit_address_field = ft.TextField(
        hint_text="Beograd, Srbija",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400)
    )
    edit_membership_type_field = ft.Dropdown(
        hint_text="Izaberite tip članstva",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        options=[
            ft.dropdown.Option("regular", "Redovno"),
            ft.dropdown.Option("student", "Studentsko"),
            ft.dropdown.Option("senior", "Penzionersko")
        ]
    )
    edit_membership_status_field = ft.Dropdown(
        hint_text="Izaberite status",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        options=[
            ft.dropdown.Option("active", "Aktivno"),
            ft.dropdown.Option("suspended", "Suspendovano"),
            ft.dropdown.Option("expired", "Isteklo")
        ]
    )
    
    # Custom modal overlays
    # Add member modal
    add_modal_overlay = ft.Container(
        content=ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Text("Dodaj novog člana", size=20, weight=ft.FontWeight.BOLD, expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            on_click=lambda e: close_add_dialog(),
                            tooltip="Zatvori"
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_300)),
                    padding=ft.padding.only(bottom=20),
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Ime *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        first_name_field,
                        ft.Text("Prezime *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        last_name_field,
                        ft.Text("Email *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        email_field,
                        ft.Text("Telefon", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        phone_field,
                        ft.Text("Adresa", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        address_field,
                        ft.Text("Tip članstva", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        membership_type_field,
                        ft.Text("Status članstva", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        membership_status_field
                    ], spacing=5, scroll=ft.ScrollMode.AUTO),
                    padding=ft.padding.only(top=10),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton("Otkaži", on_click=lambda e: close_add_dialog()),
                        ft.ElevatedButton("Dodaj", on_click=lambda e: save_member(), style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)),
                    ], alignment=ft.MainAxisAlignment.END, spacing=10),
                    border=ft.border.only(top=ft.border.BorderSide(1, ft.Colors.GREY_300)),
                    padding=ft.padding.only(top=20),
                ),
            ], spacing=20),
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            width=500 if not is_mobile else 350,
            margin=ft.margin.only(top=20, bottom=20),
        ),
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        visible=False,
    )
    
    # Edit member modal
    edit_modal_overlay = ft.Container(
        content=ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Text("Izmeni člana", size=20, weight=ft.FontWeight.BOLD, expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            on_click=lambda e: close_edit_dialog(),
                            tooltip="Zatvori"
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_300)),
                    padding=ft.padding.only(bottom=20),
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Ime *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_first_name_field,
                        ft.Text("Prezime *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_last_name_field,
                        ft.Text("Email *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_email_field,
                        ft.Text("Telefon", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_phone_field,
                        ft.Text("Adresa", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_address_field,
                        ft.Text("Tip članstva", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_membership_type_field,
                        ft.Text("Status članstva", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_membership_status_field
                    ], spacing=5, scroll=ft.ScrollMode.AUTO),
                    padding=ft.padding.only(top=10),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton("Otkaži", on_click=lambda e: close_edit_dialog()),
                        ft.ElevatedButton("Sačuvaj", on_click=lambda e: update_member_action(), style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)),
                    ], alignment=ft.MainAxisAlignment.END, spacing=10),
                    border=ft.border.only(top=ft.border.BorderSide(1, ft.Colors.GREY_300)),
                    padding=ft.padding.only(top=20),
                ),
            ], spacing=20),
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            width=500 if not is_mobile else 350,
            margin=ft.margin.only(top=20, bottom=20),
        ),
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        visible=False,
    )
    
    # Delete confirmation modal
    delete_modal_overlay = ft.Container(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Potvrda brisanja", size=20, weight=ft.FontWeight.BOLD, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        on_click=lambda e: close_delete_dialog(),
                        tooltip="Zatvori"
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text("Da li ste sigurni da želite da obrišete ovog člana?", size=16),
                ft.Row([
                    ft.ElevatedButton("Otkaži", on_click=lambda e: close_delete_dialog()),
                    ft.ElevatedButton("Obriši", on_click=lambda e: confirm_delete_member(), style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)),
                ], alignment=ft.MainAxisAlignment.END, spacing=10),
            ], spacing=10),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            width=400 if not is_mobile else 300,
            height=200,
        ),
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        visible=False,
    )
    
    # Variable to store member being deleted
    current_deleting_member_id = None
    current_editing_member_id = None
    
    def validate_field(field, error_message):
        """Validate a field and show/hide error styling"""
        if not field.value or field.value.strip() == "":
            field.border_color = ft.Colors.RED
            field.error_text = error_message
        else:
            field.border_color = None
            field.error_text = None
        page.update()
    
    def validate_all_fields():
        """Validate all required fields and return True if all valid"""
        is_valid = True
        
        # Validate add fields
        if not first_name_field.value or first_name_field.value.strip() == "":
            first_name_field.border_color = ft.Colors.RED
            first_name_field.error_text = "Ime je obavezno"
            is_valid = False
        
        if not last_name_field.value or last_name_field.value.strip() == "":
            last_name_field.border_color = ft.Colors.RED
            last_name_field.error_text = "Prezime je obavezno"
            is_valid = False
        
        if not email_field.value or email_field.value.strip() == "":
            email_field.border_color = ft.Colors.RED
            email_field.error_text = "Email je obavezan"
            is_valid = False
        
        page.update()
        return is_valid
    
    def validate_all_edit_fields():
        """Validate all required edit fields and return True if all valid"""
        is_valid = True
        
        # Validate edit fields
        if not edit_first_name_field.value or edit_first_name_field.value.strip() == "":
            edit_first_name_field.border_color = ft.Colors.RED
            edit_first_name_field.error_text = "Ime je obavezno"
            is_valid = False
        
        if not edit_last_name_field.value or edit_last_name_field.value.strip() == "":
            edit_last_name_field.border_color = ft.Colors.RED
            edit_last_name_field.error_text = "Prezime je obavezno"
            is_valid = False
        
        if not edit_email_field.value or edit_email_field.value.strip() == "":
            edit_email_field.border_color = ft.Colors.RED
            edit_email_field.error_text = "Email je obavezan"
            is_valid = False
        
        page.update()
        return is_valid
    
    def open_add_dialog():
        try:
            add_modal_overlay.visible = True
            page.update()
        except Exception as e:
            show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
    
    def close_add_dialog():
        add_modal_overlay.visible = False
        page.update()
    
    def open_edit_dialog(member_data):
        # Prepopulate fields with member data
        edit_first_name_field.value = member_data.get('first_name', '')
        edit_last_name_field.value = member_data.get('last_name', '')
        edit_email_field.value = member_data.get('email', '')
        edit_phone_field.value = member_data.get('phone', '')
        edit_address_field.value = member_data.get('address', '')
        edit_membership_type_field.value = member_data.get('membership_type', 'regular')
        edit_membership_status_field.value = member_data.get('membership_status', 'active')
        
        # Show the edit modal
        edit_modal_overlay.visible = True
        page.update()
    
    def close_edit_dialog():
        edit_modal_overlay.visible = False
        page.update()
    
    def save_member():
        try:
            # Validate all required fields first
            if not validate_all_fields():
                show_snack_bar(page, "Molimo popunite sva obavezna polja", "ERROR")
                return
            
            # Add member
            success, message = add_member(
                first_name=first_name_field.value,
                last_name=last_name_field.value,
                email=email_field.value,
                phone=phone_field.value or "",
                address=address_field.value or "",
                membership_number=f"MEM{len(members_data) + 1:03d}",
                membership_type=membership_type_field.value or "regular"
            )
            
            if success:
                show_snack_bar(page, "Član uspešno dodat!", "SUCCESS")
                close_add_dialog()
                clear_dialog_fields()
                refresh_members_list()
            else:
                show_snack_bar(page, f"Greška: {message}", "ERROR")
                
        except Exception as e:
            show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
    
    def update_member_action():
        try:
            # Validate all required fields first
            if not validate_all_edit_fields():
                show_snack_bar(page, "Molimo popunite sva obavezna polja", "ERROR")
                return
            
            # Update member
            success, message = update_member(
                member_id=current_editing_member_id,
                first_name=edit_first_name_field.value,
                last_name=edit_last_name_field.value,
                phone=edit_phone_field.value or "",
                address=edit_address_field.value or "",
                membership_type=edit_membership_type_field.value or "regular",
                membership_status=edit_membership_status_field.value or "active"
            )
            
            if success:
                show_snack_bar(page, "Član uspešno ažuriran!", "SUCCESS")
                close_edit_dialog()
                clear_edit_dialog_fields()
                refresh_members_list()
            else:
                show_snack_bar(page, f"Greška: {message}", "ERROR")
                
        except Exception as e:
            show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
    
    def clear_dialog_fields():
        first_name_field.value = ""
        last_name_field.value = ""
        email_field.value = ""
        phone_field.value = ""
        address_field.value = ""
        membership_type_field.value = None
        membership_status_field.value = None
        
        # Clear validation errors
        first_name_field.border_color = None
        first_name_field.error_text = None
        last_name_field.border_color = None
        last_name_field.error_text = None
        email_field.border_color = None
        email_field.error_text = None
        
        page.update()
    
    def clear_edit_dialog_fields():
        edit_first_name_field.value = ""
        edit_last_name_field.value = ""
        edit_email_field.value = ""
        edit_phone_field.value = ""
        edit_address_field.value = ""
        edit_membership_type_field.value = None
        edit_membership_status_field.value = None
        
        # Clear validation errors
        edit_first_name_field.border_color = None
        edit_first_name_field.error_text = None
        edit_last_name_field.border_color = None
        edit_last_name_field.error_text = None
        edit_email_field.border_color = None
        edit_email_field.error_text = None
        
        page.update()
    
    def edit_member(member_id):
        nonlocal current_editing_member_id
        current_editing_member_id = member_id
        
        # Find the member data
        member_data = None
        for member in members_data:
            if member.get('id') == member_id:
                member_data = member
                break
        
        if member_data:
            open_edit_dialog(member_data)
        else:
            show_snack_bar(page, "Član nije pronađen", "ERROR")
    
    def delete_member_confirm(member_id):
        nonlocal current_deleting_member_id
        current_deleting_member_id = member_id
        
        # Show the delete confirmation modal
        delete_modal_overlay.visible = True
        page.update()
    
    def close_delete_dialog():
        delete_modal_overlay.visible = False
        page.update()
    
    def confirm_delete_member():
        try:
            success, message = delete_member(current_deleting_member_id)
            if success:
                show_snack_bar(page, "Član uspešno obrisan!", "SUCCESS")
                refresh_members_list()
            else:
                show_snack_bar(page, f"Greška pri brisanju člana: {message}", "ERROR")
        except Exception as e:
            show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
        finally:
            close_delete_dialog()
    

    
    def refresh_members_list():
        nonlocal members_data
        members_data = get_all_members()
        update_members_list(members_data)
    
    def update_members_list(members_to_show):
        members_list.controls.clear()
        
        for member in members_to_show:
            status_color = {
                "active": ft.Colors.GREEN,
                "suspended": ft.Colors.ORANGE,
                "expired": ft.Colors.RED
            }.get(member.get('membership_status', 'active'), ft.Colors.BLUE)
            
            member_card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(
                                ft.Icons.PERSON,
                                color=status_color,
                                size=24,
                            ),
                            ft.Column([
                                ft.Text(
                                    f"{member.get('first_name', '')} {member.get('last_name', '')}",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"Email: {member.get('email', '')}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                ),
                                ft.Text(
                                    f"Telefon: {member.get('phone', '')}",
                                    size=12,
                                    color=ft.Colors.GREY_500,
                                ),
                                ft.Text(
                                    f"Broj članstva: {member.get('membership_number', '')}",
                                    size=12,
                                    color=ft.Colors.GREY_500,
                                ),
                            ], expand=True),
                            ft.Column([
                                ft.Text(
                                    member.get('membership_status', 'active').title(),
                                    size=12,
                                    color=status_color,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"Pozajmice: {member.get('current_loans', 0)}/{member.get('max_loans', 5)}",
                                    size=12,
                                    color=ft.Colors.GREY_500,
                                ),
                            ], horizontal_alignment=ft.CrossAxisAlignment.END),
                        ], spacing=16),
                        ft.Row([
                            ft.TextButton(
                                "Uredi",
                                icon=ft.Icons.EDIT,
                                on_click=lambda e, m=member: edit_member(m.get('id')),
                            ),
                            ft.TextButton(
                                "Obriši",
                                icon=ft.Icons.DELETE,
                                on_click=lambda e, m=member: delete_member_confirm(m.get('id')),
                                style=ft.ButtonStyle(color=ft.Colors.RED),
                            ),
                        ], alignment=ft.MainAxisAlignment.END),
                    ], spacing=12),
                    padding=16,
                ),
            )
            members_list.controls.append(member_card)
        
        page.update()
    
    def search_members(e):
        query = e.control.value.lower() if e.control.value else ""
        if not query:
            update_members_list(members_data)
            return
        
        filtered_members = [member for member in members_data if 
                           query in member.get('first_name', '').lower() or
                           query in member.get('last_name', '').lower() or
                           query in member.get('email', '').lower() or
                           query in member.get('membership_number', '').lower()]
        update_members_list(filtered_members)
    
    # Search input
    search_tf = ft.TextField(
        label="Pretraži članove...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        on_change=search_members,
    )
    
    # Statistics
    total_members = len(members_data)
    active_members = len([m for m in members_data if m.get('membership_status') == 'active'])
    student_members = len([m for m in members_data if m.get('membership_type') == 'student'])
    
    stats_row = ft.Row([
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"{total_members}", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                    ft.Text("Ukupno članova", size=14)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(16)
            ),
            expand=True
        ),
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"{active_members}", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
                    ft.Text("Aktivnih članova", size=14)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(16)
            ),
            expand=True
        ),
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"{student_members}", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE),
                    ft.Text("Studenata", size=14)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(16)
            ),
            expand=True
        )
    ])
    
    # Members list
    members_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    # Header with search and add button
    header_row = ft.Row([
        search_tf,
        ft.ElevatedButton(
            "Dodaj člana",
            icon=ft.Icons.ADD,
            on_click=lambda e: open_add_dialog()
        )
    ])
    
    # Initialize the list
    refresh_members_list()
    
    return ft.Stack([
        ft.Column([
            navbar_content,
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("Upravljanje članovima", size=24, weight=ft.FontWeight.BOLD),
                        padding=ft.padding.only(bottom=16)
                    ),
                    stats_row,
                    ft.Container(height=16),
                    header_row,
                    ft.Container(height=16),
                    members_list
                ], scroll=ft.ScrollMode.AUTO, expand=True),
                padding=20,
                expand=True,
            )
        ], expand=True),
        add_modal_overlay,  # Add the modal overlay on top
        edit_modal_overlay,
        delete_modal_overlay
    ], expand=True)
