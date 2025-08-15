import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import SnackBar
from utils.global_state import global_state
from datetime import datetime, timedelta

def admin_loans(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Biblioteka | Upravljanje pozajmicama"
    navbar_content = NavBar("admin", page_data)
    
    # Get loans from global state or initialize with sample data
    loans = global_state.get("loans", [])
    
    # If no loans exist, initialize with sample data
    if not loans:
        loans = [
            {
                "id": 1,
                "book_id": 1,
                "book_title": "Ana Karenjina",
                "member_id": 1,
                "member_name": "Ana Petrović",
                "loan_date": "2024-01-15",
                "due_date": "2024-01-29",
                "status": "active"
            },
            {
                "id": 2,
                "book_id": 2,
                "book_title": "Rat i mir",
                "member_id": 2,
                "member_name": "Marko Jovanović",
                "loan_date": "2024-01-10",
                "due_date": "2024-01-24",
                "status": "active"
            },
            {
                "id": 3,
                "book_id": 3,
                "book_title": "Zločin i kazna",
                "member_id": 3,
                "member_name": "Jelena Nikolić",
                "loan_date": "2024-01-20",
                "due_date": "2024-02-03",
                "status": "active"
            }
        ]
        global_state.set("loans", loans)
    
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
        # Find the loan in the loans list and update it
        for i, l in enumerate(loans):
            if l['id'] == loan_data['id']:
                loans[i]['status'] = 'returned'
                break

        
        # Update book availability
        books = global_state.get("books", [])
        for book in books:
            if book['id'] == loan['book_id']:
                book['available_copies'] += 1
                break
        global_state.set("books", books)
        
        # Save loans
        global_state.set("loans", loans)
        
        page.overlay.append(
            SnackBar("Knjiga je uspešno vraćena!", duration=3000)
        )
        update_loans_list(loans)
        page.update()
    
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
        page.overlay.append(
            SnackBar("Pozajmica je uspešno ažurirana!", duration=3000)
        )
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
        # Find and remove the loan from the loans list
        for i, l in enumerate(loans):
            if l['id'] == loan_data['id']:
                loans.pop(i)
                break
        global_state.set("loans", loans)
        page.overlay.append(
            SnackBar("Pozajmica je uspešno obrisana!", duration=3000)
        )
        close_dialog()
        update_loans_list(loans)
        page.update()
    
    def close_dialog():
        page.dialog.open = False
        page.update()
    
    def add_new_loan(e):
        # Get available books and members
        books = global_state.get("books", [])
        members = global_state.get("members", [])
        
        # Filter available books (with available copies)
        available_books = [book for book in books if book['available_copies'] > 0]
        active_members = [member for member in members if member['membership_status'] == 'active']
        
        if not available_books:
            page.overlay.append(
                SnackBar("Nema dostupnih knjiga za pozajmljivanje!", duration=3000)
            )
            page.update()
            return
        
        if not active_members:
            page.overlay.append(
                SnackBar("Nema aktivnih članova!", duration=3000)
            )
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
                page.overlay.append(
                    SnackBar("Molimo izaberite knjigu i člana!", duration=3000)
                )
                page.update()
                return
            
            # Get selected book and member
            selected_book = next((book for book in available_books if str(book['id']) == book_dropdown.value), None)
            selected_member = next((member for member in active_members if str(member['id']) == member_dropdown.value), None)
            
            if not selected_book or not selected_member:
                page.overlay.append(
                    SnackBar("Greška pri izboru knjige ili člana!", duration=3000)
                )
                page.update()
                return
            
            # Check if member can borrow more books
            member_loans = [loan for loan in loans if loan['member_id'] == selected_member['id'] and loan['status'] == 'active']
            if len(member_loans) >= selected_member['max_loans']:
                page.overlay.append(
                    SnackBar(f"Član je dostigao maksimalan broj pozajmica ({selected_member['max_loans']})!", duration=3000)
                )
                page.update()
                return
            
            # Calculate dates
            loan_date = datetime.now()
            due_date = loan_date + timedelta(days=int(loan_duration.value))
            
            # Create new loan
            new_loan = {
                "id": len(loans) + 1,
                "book_id": selected_book['id'],
                "book_title": selected_book['title'],
                "member_id": selected_member['id'],
                "member_name": f"{selected_member['first_name']} {selected_member['last_name']}",
                "loan_date": loan_date.strftime("%Y-%m-%d"),
                "due_date": due_date.strftime("%Y-%m-%d"),
                "status": "active"
            }
            
            # Add loan to list
            loans.append(new_loan)
            
            # Update book availability
            selected_book['available_copies'] -= 1
            
            # Update member's current loans
            selected_member['current_loans'] += 1
            
            # Save all changes
            global_state.set("loans", loans)
            global_state.set("books", books)
            global_state.set("members", members)
            
            page.overlay.append(
                SnackBar("Nova pozajmica je uspešno kreirana!", duration=3000)
            )
            close_dialog()
            update_loans_list(loans)
            page.update()
        
        # Create dialog
        dialog = ft.AlertDialog(
            title=ft.Text("Nova pozajmica"),
            content=ft.Column([
                ft.Text("Izaberite knjigu i člana za novu pozajmicu:", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(height=16),
                book_dropdown,
                ft.Container(height=8),
                member_dropdown,
                ft.Container(height=8),
                loan_duration,
            ], scroll=ft.ScrollMode.AUTO, height=300),
            actions=[
                ft.TextButton("Otkaži", on_click=lambda _: close_dialog()),
                ft.TextButton("Kreiraj pozajmicu", on_click=save_new_loan),
            ],
        )
        
        page.dialog = dialog
        dialog.open = True
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
    ])
