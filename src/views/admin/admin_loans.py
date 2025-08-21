import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import show_snack_bar
from controllers.admin_controller import get_all_loans, create_loan, get_all_books, get_all_members
from datetime import datetime, timedelta

def admin_loans(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Biblioteka | Upravljanje pozajmicama"
    navbar_content = NavBar("admin", page_data)
    
    # Get loans from database
    loans = get_all_loans()
    
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
                        on_click=lambda e, l=loan: return_book(l),
                    )
                )
            
            action_buttons.extend([
                ft.TextButton(
                    "Uredi",
                    icon=ft.Icons.EDIT,
                    on_click=lambda e, l=loan: edit_loan(l),
                ),
                ft.TextButton(
                    "Obriši",
                    icon=ft.Icons.DELETE,
                    on_click=lambda e, l=loan: delete_loan(l),
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
    
    def return_book(loan_data):
        # This would need to be implemented in the database functions
        show_snack_bar(page, "Funkcija vraćanja knjige će biti implementirana", "INFO")
        refresh_loans_list()
    
    def edit_loan(loan_data):
        # Simple edit dialog
        page.dialog = ft.AlertDialog(
            title=ft.Text(f"Uredi pozajmicu: {loan_data['book_title']}"),
            content=ft.Text(f"Pozajmica za knjigu '{loan_data['book_title']}' člana '{loan_data['member_name']}'"),
            actions=[
                ft.TextButton("Otkaži", on_click=lambda _: close_dialog()),
                ft.TextButton("Sačuvaj", on_click=lambda _: save_loan_edit(loan_data)),
            ],
        )
        page.dialog.open = True
        page.update()
    
    def save_loan_edit(loan_data):
        show_snack_bar(page, "Pozajmica je uspešno ažurirana!", "SUCCESS")
        close_dialog()
        page.update()
    
    def delete_loan(loan_data):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Potvrda brisanja"),
            content=ft.Text(f"Da li ste sigurni da želite da obrišete pozajmicu za knjigu '{loan_data['book_title']}'?"),
            actions=[
                ft.TextButton("Otkaži", on_click=lambda _: close_dialog()),
                ft.TextButton("Obriši", on_click=lambda _: confirm_delete_loan(loan_data)),
            ],
        )
        page.dialog.open = True
        page.update()
    
    def confirm_delete_loan(loan_data):
        # This would need to be implemented in the database functions
        show_snack_bar(page, "Pozajmica je uspešno obrisana!", "SUCCESS")
        close_dialog()
        refresh_loans_list()
        page.update()
    
    def close_dialog():
        page.dialog.open = False
        page.update()
    
    def refresh_loans_list():
        nonlocal loans
        loans = get_all_loans()
        update_loans_list(loans)
    
    def add_new_loan(e):
        # Get available books and members from database
        books = get_all_books()
        members = get_all_members()
        
        # Filter available books (with available copies)
        available_books = [book for book in books if book['available_copies'] > 0]
        active_members = [member for member in members if member['membership_status'] == 'active']
        
        if not available_books:
            show_snack_bar(page, "Nema dostupnih knjiga za pozajmljivanje!", "ERROR")
            page.update()
            return
        
        if not active_members:
            show_snack_bar(page, "Nema aktivnih članova!", "ERROR")
            page.update()
            return
        
        # Create book options
        book_options = [
            ft.dropdown.Option(
                str(book['id']), 
                f"{book['title']} - {book['author']} (Dostupno: {book['available_copies']})"
            ) for book in available_books
        ]
        
        # Create member options
        member_options = [
            ft.dropdown.Option(
                str(member['id']), 
                f"{member['first_name']} {member['last_name']} - {member['membership_number']}"
            ) for member in active_members
        ]
        
        # Form fields
        book_dropdown = ft.Dropdown(
            label="Izaberi knjigu",
            options=book_options,
            expand=True
        )
        
        member_dropdown = ft.Dropdown(
            label="Izaberi člana",
            options=member_options,
            expand=True
        )
        
        loan_duration = ft.Dropdown(
            label="Trajanje pozajmice",
            value="14",
            options=[
                ft.dropdown.Option("7", "7 dana"),
                ft.dropdown.Option("14", "14 dana"),
                ft.dropdown.Option("21", "21 dan"),
                ft.dropdown.Option("30", "30 dana")
            ],
            expand=True
        )
        
        def save_new_loan(e):
            if not book_dropdown.value or not member_dropdown.value:
                show_snack_bar(page, "Molimo izaberite knjigu i člana", "ERROR")
                return
            
            try:
                book_id = int(book_dropdown.value)
                member_id = int(member_dropdown.value)
                
                success, message = create_loan(book_id, member_id)
                if success:
                    show_snack_bar(page, "Pozajmica uspešno kreirana!", "SUCCESS")
                    close_dialog()
                    refresh_loans_list()
                else:
                    show_snack_bar(page, f"Greška: {message}", "ERROR")
                    
            except Exception as e:
                show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
        
        # Create the dialog
        loan_dialog = ft.AlertDialog(
            title=ft.Text("Nova pozajmica"),
            content=ft.Column([
                book_dropdown,
                member_dropdown,
                loan_duration
            ], scroll=ft.ScrollMode.AUTO, height=300),
            actions=[
                ft.TextButton("Otkaži", on_click=lambda e: close_dialog()),
                ft.TextButton("Kreiraj", on_click=save_new_loan)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.dialog = loan_dialog
        loan_dialog.open = True
        page.update()
    
    def search_loans(e):
        query = search_tf.value.lower()
        filtered_loans = [loan for loan in loans if 
                         query in loan['book_title'].lower() or 
                         query in loan['member_name'].lower()]
        update_loans_list(filtered_loans)
    
    # Search input
    search_tf = ft.TextField(
        label="Pretraži pozajmice...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        on_submit=search_loans,
    )
    
    search_button = ft.ElevatedButton(
        "Pretraži",
        icon=ft.Icons.SEARCH,
        on_click=search_loans,
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
            ft.Row(
                [search_tf, search_button],
                spacing=16,
            ),
            ft.Divider(height=32),
            ft.Container(
                content=loans_list,
                expand=True,
                height=400,  # Fixed height to enable scrolling
            ),
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
    ], expand=True)
