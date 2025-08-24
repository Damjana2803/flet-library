import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import show_snack_bar
from controllers.admin_controller import get_all_loans, create_loan, get_all_books, get_all_members, return_loan, update_loan, delete_loan
from datetime import datetime, timedelta

def admin_loans(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Biblioteka | Upravljanje pozajmicama"
    navbar_content = NavBar("admin", page_data)
    
    # Check if mobile screen
    is_mobile = page.width < 768 if page.width else False
    
    # Get loans from database
    loans = get_all_loans()
    
    # Dialog fields for adding new loan
    book_dropdown_field = ft.Dropdown(
        hint_text="Izaberite knjigu",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        options=[],
        expand=True,
        # menu_height=400,
        on_change=lambda e: validate_field(book_dropdown_field, "Knjiga je obavezna")
    )
    member_dropdown_field = ft.Dropdown(
        hint_text="Izaberite člana",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        options=[],
        expand=True,
        # menu_height=400,
        on_change=lambda e: validate_field(member_dropdown_field, "Član je obavezan")
    )
    loan_duration_field = ft.Dropdown(
        hint_text="Izaberite trajanje",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        value="14",
        expand=True,
        options=[
            ft.dropdown.Option("7", "7 dana"),
            ft.dropdown.Option("14", "14 dana"),
            ft.dropdown.Option("21", "21 dan"),
            ft.dropdown.Option("30", "30 dana")
        ]
    )
    
    # Edit loan dialog fields
    edit_due_date_field = ft.TextField(
        hint_text="YYYY-MM-DD",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(edit_due_date_field, "Datum je obavezan")
    )
    
    # Custom modal overlays
    # Add loan modal
    add_modal_overlay = ft.Container(
        content=ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Text("Nova pozajmica", size=20, weight=ft.FontWeight.BOLD, expand=True),
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
                        ft.Text("Knjiga *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        book_dropdown_field,
                        ft.Text("Član *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        member_dropdown_field,
                        ft.Text("Trajanje pozajmice", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        loan_duration_field
                    ], spacing=5, scroll=ft.ScrollMode.AUTO),
                    padding=ft.padding.only(top=10),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton("Otkaži", on_click=lambda e: close_add_dialog()),
                        ft.ElevatedButton("Kreiraj", on_click=lambda e: save_loan(), style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)),
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
    
    # Edit loan modal
    edit_modal_overlay = ft.Container(
        content=ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Text("Izmeni pozajmicu", size=20, weight=ft.FontWeight.BOLD, expand=True),
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
                        ft.Text("Datum vraćanja *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_due_date_field
                    ], spacing=5, scroll=ft.ScrollMode.AUTO),
                    padding=ft.padding.only(top=10),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton("Otkaži", on_click=lambda e: close_edit_dialog()),
                        ft.ElevatedButton("Sačuvaj", on_click=lambda e: update_loan_action(), style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)),
                    ], alignment=ft.MainAxisAlignment.END, spacing=10),
                    border=ft.border.only(top=ft.border.BorderSide(1, ft.Colors.GREY_300)),
                    padding=ft.padding.only(top=20),
                ),
            ], spacing=20),
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            width=400 if not is_mobile else 320,
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
                ft.Text("Da li ste sigurni da želite da obrišete ovu pozajmicu?", size=16),
                ft.Row([
                    ft.ElevatedButton("Otkaži", on_click=lambda e: close_delete_dialog()),
                    ft.ElevatedButton("Obriši", on_click=lambda e: confirm_delete_loan(), style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)),
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
    
    # Return book confirmation modal
    return_modal_overlay = ft.Container(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Potvrda vraćanja", size=20, weight=ft.FontWeight.BOLD, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        on_click=lambda e: close_return_dialog(),
                        tooltip="Zatvori"
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text("Da li ste sigurni da želite da označite ovu knjigu kao vraćenu?", size=16),
                ft.Row([
                    ft.ElevatedButton("Otkaži", on_click=lambda e: close_return_dialog()),
                    ft.ElevatedButton("Vrati knjigu", on_click=lambda e: confirm_return_book(), style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)),
                ], alignment=ft.MainAxisAlignment.END, spacing=10),
            ], spacing=10),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            width=450 if not is_mobile else 320,
            height=200,
        ),
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        visible=False,
    )
    
    # Variables to store current operations
    current_deleting_loan_id = None
    current_editing_loan_id = None
    current_returning_loan_id = None
    
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
        
        if not book_dropdown_field.value:
            book_dropdown_field.border_color = ft.Colors.RED
            book_dropdown_field.error_text = "Knjiga je obavezna"
            is_valid = False
        
        if not member_dropdown_field.value:
            member_dropdown_field.border_color = ft.Colors.RED
            member_dropdown_field.error_text = "Član je obavezan"
            is_valid = False
        
        page.update()
        return is_valid
    
    def validate_edit_fields():
        """Validate edit fields and return True if all valid"""
        is_valid = True
        
        if not edit_due_date_field.value or edit_due_date_field.value.strip() == "":
            edit_due_date_field.border_color = ft.Colors.RED
            edit_due_date_field.error_text = "Datum je obavezan"
            is_valid = False
        
        page.update()
        return is_valid
    
    def open_add_dialog():
        try:
            # Populate dropdowns with current data
            books = get_all_books()
            members = get_all_members()
            
            # Filter available books (with available copies)
            available_books = [book for book in books if book.get('available_copies', 0) > 0]
            active_members = [member for member in members if member.get('membership_status') == 'active']
            
            if not available_books:
                show_snack_bar(page, "Nema dostupnih knjiga za pozajmljivanje!", "ERROR")
                return
            
            if not active_members:
                show_snack_bar(page, "Nema aktivnih članova!", "ERROR")
                return
            
            # Update dropdown options
            book_dropdown_field.options = [
                ft.dropdown.Option(
                    str(book['id']), 
                    f"{book['title']} - {book['author']} (Dostupno: {book['available_copies']})"
                ) for book in available_books
            ]
            
            member_dropdown_field.options = [
                ft.dropdown.Option(
                    str(member['id']), 
                    f"{member['first_name']} {member['last_name']} - {member['membership_number']}"
                ) for member in active_members
            ]
            
            add_modal_overlay.visible = True
            page.update()
        except Exception as e:
            show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
    
    def close_add_dialog():
        add_modal_overlay.visible = False
        page.update()
    
    def open_edit_dialog(loan_data):
        # Prepopulate fields with loan data
        edit_due_date_field.value = loan_data.get('due_date', '')
        
        # Show the edit modal
        edit_modal_overlay.visible = True
        page.update()
    
    def close_edit_dialog():
        edit_modal_overlay.visible = False
        page.update()
    
    def open_return_dialog(loan_id):
        nonlocal current_returning_loan_id
        current_returning_loan_id = loan_id
        return_modal_overlay.visible = True
        page.update()
    
    def close_return_dialog():
        return_modal_overlay.visible = False
        page.update()
    
    def open_delete_dialog(loan_id):
        nonlocal current_deleting_loan_id
        current_deleting_loan_id = loan_id
        delete_modal_overlay.visible = True
        page.update()
    
    def close_delete_dialog():
        delete_modal_overlay.visible = False
        page.update()
    
    def save_loan():
        try:
            # Validate all required fields first
            if not validate_all_fields():
                show_snack_bar(page, "Molimo popunite sva obavezna polja", "ERROR")
                return
            
            # Create loan
            book_id = int(book_dropdown_field.value)
            member_id = int(member_dropdown_field.value)
            
            success, message = create_loan(book_id, member_id)
            
            if success:
                show_snack_bar(page, "Pozajmica uspešno kreirana!", "SUCCESS")
                close_add_dialog()
                clear_dialog_fields()
                # Clear search and refresh list
                search_tf.value = ""
                refresh_loans_list()
            else:
                # Check if it's a loan limit error and display with orange warning color
                if "maksimalan broj pozajmica" in message:
                    show_snack_bar(page, f"Greška: {message}", "WARNING")
                else:
                    show_snack_bar(page, f"Greška: {message}", "ERROR")
                
        except Exception as e:
            show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
    
    def update_loan_action():
        try:
            # Validate edit fields first
            if not validate_edit_fields():
                show_snack_bar(page, "Molimo popunite sva obavezna polja", "ERROR")
                return
            
            # Update loan
            success, message = update_loan(current_editing_loan_id, edit_due_date_field.value)
            
            if success:
                show_snack_bar(page, "Pozajmica uspešno ažurirana!", "SUCCESS")
                close_edit_dialog()
                clear_edit_dialog_fields()
                # Clear search and refresh list
                search_tf.value = ""
                refresh_loans_list()
            else:
                show_snack_bar(page, f"Greška: {message}", "ERROR")
                
        except Exception as e:
            show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
    
    def confirm_return_book():
        try:
            success, message = return_loan(current_returning_loan_id)
            if success:
                show_snack_bar(page, "Knjiga uspešno vraćena!", "SUCCESS")
                # Clear search and refresh list
                search_tf.value = ""
                refresh_loans_list()
            else:
                show_snack_bar(page, f"Greška: {message}", "ERROR")
        except Exception as e:
            show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
        finally:
            close_return_dialog()
    
    def confirm_delete_loan():
        try:
            success, message = delete_loan(current_deleting_loan_id)
            if success:
                show_snack_bar(page, "Pozajmica uspešno obrisana!", "SUCCESS")
                # Clear search and refresh list
                search_tf.value = ""
                refresh_loans_list()
            else:
                show_snack_bar(page, f"Greška: {message}", "ERROR")
        except Exception as e:
            show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
        finally:
            close_delete_dialog()
    
    def clear_dialog_fields():
        book_dropdown_field.value = None
        member_dropdown_field.value = None
        loan_duration_field.value = "14"
        
        # Clear validation errors
        book_dropdown_field.border_color = None
        book_dropdown_field.error_text = None
        member_dropdown_field.border_color = None
        member_dropdown_field.error_text = None
        
        page.update()
    
    def clear_edit_dialog_fields():
        edit_due_date_field.value = ""
        
        # Clear validation errors
        edit_due_date_field.border_color = None
        edit_due_date_field.error_text = None
        
        page.update()
    
    def edit_loan_action(loan_id):
        nonlocal current_editing_loan_id
        current_editing_loan_id = loan_id
        
        # Find the loan data
        loan_data = None
        for loan in loans:
            if loan.get('id') == loan_id:
                loan_data = loan
                break
        
        if loan_data:
            open_edit_dialog(loan_data)
        else:
            show_snack_bar(page, "Pozajmica nije pronađena", "ERROR")
    
    def refresh_loans_list():
        nonlocal loans
        loans = get_all_loans()
        update_loans_list(loans)
    
    # Loans list - defined before functions that use it
    loans_list = ft.Column(
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    
    def update_loans_list(loans_to_show):
        loans_list.controls.clear()
        
        for loan in loans_to_show:
            status_color = {
                "active": ft.Colors.GREEN,
                "returned": ft.Colors.GREY
            }.get(loan['status'], ft.Colors.BLUE)
            
            # Create action buttons based on loan status
            action_buttons = []
            
            if loan['status'] == 'active':
                action_buttons.append(
                    ft.TextButton(
                        "Vrati knjigu",
                        icon=ft.Icons.CHECK_CIRCLE,
                        on_click=lambda e, loan_id=loan.get('id'): open_return_dialog(loan_id),
                    )
                )
            
            action_buttons.extend([
                ft.TextButton(
                    "Uredi",
                    icon=ft.Icons.EDIT,
                    on_click=lambda e, loan_id=loan.get('id'): edit_loan_action(loan_id),
                ),
                ft.TextButton(
                    "Obriši",
                    icon=ft.Icons.DELETE,
                    on_click=lambda e, loan_id=loan.get('id'): open_delete_dialog(loan_id),
                ),
            ])
            
            loan_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.LIBRARY_BOOKS,
                                        color=status_color,
                                        size=24,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(
                                                loan['book_title'],
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(
                                                f"Član: {loan['member_name']}",
                                                size=14,
                                                color=ft.Colors.GREY_600,
                                            ),
                                            ft.Text(
                                                f"Datum pozajmice: {loan['loan_date']}",
                                                size=12,
                                                color=ft.Colors.GREY_500,
                                            ),
                                            ft.Text(
                                                f"Datum vraćanja: {loan['due_date']}",
                                                size=12,
                                                color=ft.Colors.GREY_500,
                                            ),
                                        ],
                                        expand=True,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(
                                                loan['status'].title(),
                                                size=12,
                                                color=status_color,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.END,
                                    ),
                                ],
                                spacing=16,
                            ),
                            ft.Row(
                                action_buttons,
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ],
                        spacing=12,
                    ),
                    padding=16,
                ),
            )
            loans_list.controls.append(loan_card)
        
        page.update()
    

    
    def add_new_loan(e):
        open_add_dialog()
    
    def search_loans(e):
        query = e.control.value.lower() if e.control.value else ""
        if not query:
            update_loans_list(loans)
            return
        
        filtered_loans = [loan for loan in loans if 
                         query in loan['book_title'].lower() or 
                         query in loan['member_name'].lower()]
        update_loans_list(filtered_loans)
    
    # Search input
    search_tf = ft.TextField(
        label="Pretraži pozajmice...",
        prefix_icon=ft.Icons.SEARCH,
        # expand=True,
        height=50,
        on_change=search_loans,
        on_submit=search_loans,
    )
    
    # Initialize loans list
    update_loans_list(loans)
    
    # Main content
    content = ft.Column(
        [
            ft.Row(
                [
                    ft.Text(
                        "Upravljanje pozajmicama",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),
                    ft.ElevatedButton(
                        "Nova pozajmica",
                        icon=ft.Icons.ADD,
                        on_click=add_new_loan,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            search_tf,
            ft.Container(
                content=loans_list,
                expand=True,
            ),
        ],
        spacing=16,
        expand=True,
    )
    
    return ft.Stack([
        ft.Column([
            navbar_content,
            ft.Container(
                content=content,
                padding=20,
                expand=True,
            )
        ], expand=True),
        add_modal_overlay,  # Add the modal overlays on top
        edit_modal_overlay,
        delete_modal_overlay,
        return_modal_overlay
    ], expand=True)
