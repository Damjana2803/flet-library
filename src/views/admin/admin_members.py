import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import SnackBar
from models.member import Member
from utils.global_state import global_state
from datetime import datetime

def admin_members(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Biblioteka | Upravljanje članovima"
    navbar_content = NavBar("admin", page_data)
    
    # Get members from global state or initialize with sample data
    members_data = global_state.get("members", [])
    
    # If no members exist, initialize with sample data
    if not members_data:
        members_data = [
            {
                "id": 1,
                "first_name": "Ana",
                "last_name": "Petrović",
                "email": "ana.petrovic@email.com",
                "phone": "+381 11 123 4567",
                "address": "Beograd, Srbija",
                "membership_number": "MEM001",
                "membership_type": "regular",
                "membership_status": "active",
                "membership_start_date": "2023-01-15",
                "membership_end_date": "2024-01-15",
                "max_loans": 5,
                "current_loans": 2
            },
            {
                "id": 2,
                "first_name": "Marko",
                "last_name": "Jovanović",
                "email": "marko.jovanovic@email.com",
                "phone": "+381 11 234 5678",
                "address": "Novi Sad, Srbija",
                "membership_number": "MEM002",
                "membership_type": "student",
                "membership_status": "active",
                "membership_start_date": "2023-03-20",
                "membership_end_date": "2024-03-20",
                "max_loans": 3,
                "current_loans": 1
            },
            {
                "id": 3,
                "first_name": "Jelena",
                "last_name": "Nikolić",
                "email": "jelena.nikolic@email.com",
                "phone": "+381 11 345 6789",
                "address": "Niš, Srbija",
                "membership_number": "MEM003",
                "membership_type": "senior",
                "membership_status": "active",
                "membership_start_date": "2023-06-10",
                "membership_end_date": "2024-06-10",
                "max_loans": 7,
                "current_loans": 0
            }
        ]
        global_state.set("members", members_data)
    
    def show_member_dialog(member=None, is_edit=False):
        title = "Izmeni člana" if is_edit else "Dodaj novog člana"
        
        first_name_tf = ft.TextField(
            label="Ime",
            value=member["first_name"] if member else "",
            expand=True
        )
        last_name_tf = ft.TextField(
            label="Prezime",
            value=member["last_name"] if member else "",
            expand=True
        )
        email_tf = ft.TextField(
            label="E-adresa",
            value=member["email"] if member else "",
            expand=True
        )
        phone_tf = ft.TextField(
            label="Telefon",
            value=member["phone"] if member else "",
            expand=True
        )
        address_tf = ft.TextField(
            label="Adresa",
            value=member["address"] if member else "",
            expand=True
        )
        membership_type_dd = ft.Dropdown(
            label="Tip članstva",
            value=member["membership_type"] if member else "regular",
            options=[
                ft.dropdown.Option("regular", "Redovno"),
                ft.dropdown.Option("student", "Studentsko"),
                ft.dropdown.Option("senior", "Penzionersko")
            ],
            expand=True
        )
        membership_status_dd = ft.Dropdown(
            label="Status članstva",
            value=member["membership_status"] if member else "active",
            options=[
                ft.dropdown.Option("active", "Aktivno"),
                ft.dropdown.Option("suspended", "Suspendovano"),
                ft.dropdown.Option("expired", "Isteklo")
            ],
            expand=True
        )
        
        def save_member(e):
            if not all([first_name_tf.value, last_name_tf.value, email_tf.value]):
                page.overlay.append(SnackBar("Greška", "Popunite sva obavezna polja", "ERROR"))
                page.update()
                return
            
            if is_edit:
                # Update existing member
                member["first_name"] = first_name_tf.value
                member["last_name"] = last_name_tf.value
                member["email"] = email_tf.value
                member["phone"] = phone_tf.value
                member["address"] = address_tf.value
                member["membership_type"] = membership_type_dd.value
                member["membership_status"] = membership_status_dd.value
                page.overlay.append(SnackBar("Uspešno", "Član je ažuriran"))
            else:
                # Add new member
                new_member = {
                    "id": len(members_data) + 1,
                    "first_name": first_name_tf.value,
                    "last_name": last_name_tf.value,
                    "email": email_tf.value,
                    "phone": phone_tf.value,
                    "address": address_tf.value,
                    "membership_number": f"MEM{len(members_data) + 1:03d}",
                    "membership_type": membership_type_dd.value,
                    "membership_status": membership_status_dd.value,
                    "membership_start_date": datetime.now().strftime("%Y-%m-%d"),
                    "membership_end_date": datetime.now().replace(year=datetime.now().year + 1).strftime("%Y-%m-%d"),
                    "max_loans": 5,
                    "current_loans": 0
                }
                members_data.append(new_member)
                page.overlay.append(SnackBar("Uspešno", "Novi član je dodat"))
            
            # Save to global state
            global_state.set("members", members_data)
            
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
    
    def delete_member(member_id):
        member = next((m for m in members_data if m["id"] == member_id), None)
        if member:
            members_data.remove(member)
            # Save to global state
            global_state.set("members", members_data)
            page.overlay.append(SnackBar("Uspešno", "Član je obrisan"))
            page.update()
            refresh_members_list()
    
    def show_delete_dialog(member):
        def confirm_delete(e):
            delete_member(member["id"])
            dialog.open = False
            page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Potvrda brisanja"),
            content=ft.Text(f"Da li ste sigurni da želite da obrišete člana {member['first_name']} {member['last_name']}?"),
            actions=[
                ft.TextButton("Otkaži", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.TextButton("Obriši", on_click=confirm_delete, style=ft.ButtonStyle(color=ft.colors.RED))
            ]
        )
        
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    def refresh_members_list():
        members_list.controls.clear()
        
        for member in members_data:
            status_color = {
                "active": ft.colors.GREEN,
                "suspended": ft.colors.ORANGE,
                "expired": ft.colors.RED
            }.get(member["membership_status"], ft.colors.GREY)
            
            members_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.PERSON, color=ft.colors.BLUE),
                                title=ft.Text(f"{member['first_name']} {member['last_name']}"),
                                subtitle=ft.Text(f"Član broj: {member['membership_number']}"),
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Text(f"E-adresa: {member['email']}", size=12),
                                        ft.Text(f"Telefon: {member['phone']}", size=12),
                                    ]),
                                    ft.Row([
                                        ft.Text(f"Tip: {member['membership_type']}", size=12),
                                        ft.Container(
                                            content=ft.Text(
                                                member["membership_status"].upper(),
                                                color=ft.colors.WHITE,
                                                size=10,
                                                weight=ft.FontWeight.BOLD
                                            ),
                                            bgcolor=status_color,
                                            padding=ft.padding.all(4),
                                            border_radius=ft.border_radius.all(4)
                                        ),
                                    ]),
                                    ft.Row([
                                        ft.Text(f"Pozajmice: {member['current_loans']}/{member['max_loans']}", size=12),
                                        ft.Text(f"Članstvo do: {member['membership_end_date']}", size=12),
                                    ])
                                ]),
                                padding=ft.padding.only(left=16, right=16, bottom=16)
                            ),
                            ft.Row([
                                ft.TextButton("Izmeni", on_click=lambda m=member: show_member_dialog(m, True)),
                                ft.TextButton("Obriši", on_click=lambda m=member: show_delete_dialog(m), style=ft.ButtonStyle(color=ft.colors.RED))
                            ], alignment=ft.MainAxisAlignment.END)
                        ])
                    )
                )
            )
        
        page.update()
    
    # Search functionality
    search_tf = ft.TextField(
        label="Pretraži članove",
        prefix_icon=ft.icons.SEARCH,
        on_change=lambda e: filter_members(e.control.value),
        expand=True
    )
    
    def filter_members(search_term):
        if not search_term:
            refresh_members_list()
            return
        
        filtered_members = [
            member for member in members_data
            if search_term.lower() in f"{member['first_name']} {member['last_name']}".lower() or
               search_term.lower() in member['email'].lower() or
               search_term.lower() in member['membership_number'].lower()
        ]
        
        members_list.controls.clear()
        for member in filtered_members:
            # Same card creation logic as in refresh_members_list
            status_color = {
                "active": ft.colors.GREEN,
                "suspended": ft.colors.ORANGE,
                "expired": ft.colors.RED
            }.get(member["membership_status"], ft.colors.GREY)
            
            members_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.PERSON, color=ft.colors.BLUE),
                                title=ft.Text(f"{member['first_name']} {member['last_name']}"),
                                subtitle=ft.Text(f"Član broj: {member['membership_number']}"),
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Text(f"E-adresa: {member['email']}", size=12),
                                        ft.Text(f"Telefon: {member['phone']}", size=12),
                                    ]),
                                    ft.Row([
                                        ft.Text(f"Tip: {member['membership_type']}", size=12),
                                        ft.Container(
                                            content=ft.Text(
                                                member["membership_status"].upper(),
                                                color=ft.colors.WHITE,
                                                size=10,
                                                weight=ft.FontWeight.BOLD
                                            ),
                                            bgcolor=status_color,
                                            padding=ft.padding.all(4),
                                            border_radius=ft.border_radius.all(4)
                                        ),
                                    ]),
                                    ft.Row([
                                        ft.Text(f"Pozajmice: {member['current_loans']}/{member['max_loans']}", size=12),
                                        ft.Text(f"Članstvo do: {member['membership_end_date']}", size=12),
                                    ])
                                ]),
                                padding=ft.padding.only(left=16, right=16, bottom=16)
                            ),
                            ft.Row([
                                ft.TextButton("Izmeni", on_click=lambda m=member: show_member_dialog(m, True)),
                                ft.TextButton("Obriši", on_click=lambda m=member: show_delete_dialog(m), style=ft.ButtonStyle(color=ft.colors.RED))
                            ], alignment=ft.MainAxisAlignment.END)
                        ])
                    )
                )
            )
        
        page.update()
    
    # Statistics cards
    total_members = len(members_data)
    active_members = len([m for m in members_data if m["membership_status"] == "active"])
    student_members = len([m for m in members_data if m["membership_type"] == "student"])
    
    stats_row = ft.Row([
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"{total_members}", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE),
                    ft.Text("Ukupno članova", size=14)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(16)
            ),
            expand=True
        ),
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"{active_members}", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN),
                    ft.Text("Aktivnih", size=14)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(16)
            ),
            expand=True
        ),
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"{student_members}", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE),
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
            icon=ft.icons.ADD,
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
    ])
