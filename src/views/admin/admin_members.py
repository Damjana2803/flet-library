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
    
    def show_member_dialog(member=None, is_edit=False):
        title = "Izmeni člana" if is_edit else "Dodaj novog člana"
        
        first_name_tf = ft.TextField(
            label="Ime",
            value=member.get("first_name", "") if member else "",
            expand=True
        )
        last_name_tf = ft.TextField(
            label="Prezime",
            value=member.get("last_name", "") if member else "",
            expand=True
        )
        email_tf = ft.TextField(
            label="E-adresa",
            value=member.get("email", "") if member else "",
            expand=True
        )
        phone_tf = ft.TextField(
            label="Telefon",
            value=member.get("phone", "") if member else "",
            expand=True
        )
        address_tf = ft.TextField(
            label="Adresa",
            value=member.get("address", "") if member else "",
            expand=True
        )
        membership_type_dd = ft.Dropdown(
            label="Tip članstva",
            value=member.get("membership_type", "regular") if member else "regular",
            options=[
                ft.dropdown.Option("regular", "Redovno"),
                ft.dropdown.Option("student", "Studentsko"),
                ft.dropdown.Option("senior", "Penzionersko")
            ],
            expand=True
        )
        membership_status_dd = ft.Dropdown(
            label="Status članstva",
            value=member.get("membership_status", "active") if member else "active",
            options=[
                ft.dropdown.Option("active", "Aktivno"),
                ft.dropdown.Option("suspended", "Suspendovano"),
                ft.dropdown.Option("expired", "Isteklo")
            ],
            expand=True
        )
        
        def save_member(e):
            if not all([first_name_tf.value, last_name_tf.value, email_tf.value]):
                show_snack_bar(page, "Popunite sva obavezna polja", "ERROR")
                return
            
            if is_edit:
                # Update existing member
                success, message = update_member(
                    member_id=member["id"],
                    first_name=first_name_tf.value,
                    last_name=last_name_tf.value,
                    phone=phone_tf.value,
                    address=address_tf.value,
                    membership_type=membership_type_dd.value,
                    membership_status=membership_status_dd.value
                )
                if success:
                    show_snack_bar(page, "Član je uspešno ažuriran", "SUCCESS")
                else:
                    show_snack_bar(page, f"Greška: {message}", "ERROR")
            else:
                # Add new member
                success, message = add_member(
                    first_name=first_name_tf.value,
                    last_name=last_name_tf.value,
                    email=email_tf.value,
                    phone=phone_tf.value,
                    address=address_tf.value,
                    membership_number=f"MEM{len(members_data) + 1:03d}",
                    membership_type=membership_type_dd.value
                )
                if success:
                    show_snack_bar(page, "Novi član je uspešno dodat", "SUCCESS")
                else:
                    show_snack_bar(page, f"Greška: {message}", "ERROR")
            
            page.update()
            dialog.open = False
            refresh_members_list()
        
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Column([
                ft.Row([first_name_tf, last_name_tf]),
                email_tf,
                phone_tf,
                address_tf,
                ft.Row([membership_type_dd, membership_status_dd])
            ], scroll=ft.ScrollMode.AUTO, height=400),
            actions=[
                ft.TextButton("Otkaži", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.TextButton("Sačuvaj", on_click=save_member)
            ]
        )
        
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    def delete_member_func(member_id):
        success, message = delete_member(member_id)
        if success:
            show_snack_bar(page, "Član je uspešno obrisan", "SUCCESS")
        else:
            show_snack_bar(page, f"Greška: {message}", "ERROR")
        refresh_members_list()
    
    def show_delete_dialog(member):
        def confirm_delete(e):
            delete_member_func(member["id"])
            delete_dialog.open = False
            page.update()
        
        def cancel_delete(e):
            delete_dialog.open = False
            page.update()
        
        delete_dialog = ft.AlertDialog(
            title=ft.Text("Potvrda brisanja"),
            content=ft.Text(f"Da li ste sigurni da želite da obrišete člana {member['first_name']} {member['last_name']}?"),
            actions=[
                ft.TextButton("Otkaži", on_click=cancel_delete),
                ft.TextButton("Obriši", on_click=confirm_delete, style=ft.ButtonStyle(color=ft.Colors.RED))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.dialog = delete_dialog
        delete_dialog.open = True
        page.update()
    
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
                                on_click=lambda e, m=member: show_member_dialog(m, True),
                            ),
                            ft.TextButton(
                                "Obriši",
                                icon=ft.Icons.DELETE,
                                on_click=lambda e, m=member: show_delete_dialog(m),
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
        query = search_tf.value.lower()
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
        on_submit=search_members,
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
    members_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, height=400)
    
    # Header with search and add button
    header_row = ft.Row([
        search_tf,
        ft.ElevatedButton(
            "Dodaj člana",
            icon=ft.Icons.ADD,
            on_click=lambda e: show_member_dialog()
        )
    ])
    
    # Initialize the list
    refresh_members_list()
    
    return ft.Column([
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
    ], expand=True)
