import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import SnackBar
from datetime import datetime, timedelta

def my_loans(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Moje iznajmljene knjige - Biblioteka"
    
    # Navigation bar
    navbar_content = NavBar("member", page_data)
    
    # Get current user and loans from global state
    from utils.global_state import global_state
    
    current_user = global_state.get("user", {})
    all_loans = global_state.get("loans", [])
    
    # Filter loans for current user
    user_id = current_user.get("id")
    loans = [loan for loan in all_loans if loan.get("member_id") == user_id]
    
    # If no loans found, show empty state
    if not loans:
        loans = []
    
    def renew_loan(loan_id):
        """Renew a loan - extend the due date by 14 days"""
        from utils.global_state import global_state
        from datetime import datetime, timedelta
        
        # Get all loans
        all_loans = global_state.get("loans", [])
        
        # Find the loan and extend it
        loan_found = False
        
        for i, loan in enumerate(all_loans):
            if loan.get('id') == loan_id and loan.get('status') == 'active':
                # Calculate new due date
                current_due_date = datetime.strptime(loan.get('due_date'), "%Y-%m-%d")
                new_due_date = current_due_date + timedelta(days=14)
                
                all_loans[i]['due_date'] = new_due_date.strftime("%Y-%m-%d")
                loan_found = True
                break
        
        if not loan_found:
            page.overlay.append(
                SnackBar("Pozajmica nije pronađena ili je već vraćena!", duration=3000)
            )
            page.update()
            return
        
        # Save to global state
        global_state.set("loans", all_loans)
        
        # Show success message
        page.overlay.append(
            SnackBar("Knjiga je uspešno produžena za 14 dana!", duration=3000)
        )
        page.update()
    
    def return_book(loan_id):
        """Return a book - mark loan as returned and update book availability"""
        from utils.global_state import global_state
        from datetime import datetime
        
        # Get all loans and books
        all_loans = global_state.get("loans", [])
        all_books = global_state.get("books", [])
        current_user = global_state.get("user", {})
        
        # Find the loan and mark it as returned
        loan_found = False
        book_id = None
        
        for i, loan in enumerate(all_loans):
            if loan.get('id') == loan_id:
                all_loans[i]['status'] = 'returned'
                all_loans[i]['returned_date'] = datetime.now().strftime("%Y-%m-%d")
                book_id = loan.get('book_id')
                loan_found = True
                break
        
        if not loan_found:
            page.overlay.append(
                SnackBar("Pozajmica nije pronađena!", duration=3000)
            )
            page.update()
            return
        
        # Update book availability
        if book_id:
            for i, book in enumerate(all_books):
                if book.get('id') == book_id:
                    all_books[i]['available_copies'] = book.get('available_copies', 0) + 1
                    break
        
        # Update user's current loans count
        if current_user:
            current_user['current_loans'] = max(0, current_user.get('current_loans', 0) - 1)
            global_state.set("user", current_user)
        
        # Save to global state
        global_state.set("loans", all_loans)
        global_state.set("books", all_books)
        
        # Show success message
        page.overlay.append(
            SnackBar("Knjiga je uspešno vraćena!", duration=3000)
        )
        page.update()
    

    
    def get_status_color(status):
        if status == "returned":
            return ft.Colors.GREY
        else:
            return ft.Colors.GREEN
    
    def get_status_text(status):
        if status == "returned":
            return "Vraćeno"
        else:
            return "Aktivno"
    
    def format_date(date_str):
        if isinstance(date_str, str):
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                return date_obj.strftime("%d.%m.%Y")
            except:
                return date_str
        elif isinstance(date_str, datetime):
            return date_str.strftime("%d.%m.%Y")
        return str(date_str)
    
    def get_days_remaining(due_date_str):
        if isinstance(due_date_str, str):
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
                remaining = (due_date - datetime.now()).days
                return max(0, remaining)
            except:
                return 0
        elif isinstance(due_date_str, datetime):
            remaining = (due_date_str - datetime.now()).days
            return max(0, remaining)
        return 0
    

    
    # Loans list
    if loans:
        loans_content = [
            ft.Text(
                "Moje iznajmljene knjige",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_900,
            ),
        ] + [
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.BOOK,
                                        color=get_status_color(loan["status"]),
                                        size=24,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(
                                                loan["book_title"],
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(
                                                f"Autor: {loan['book_author']}",
                                                size=14,
                                                color=ft.Colors.GREY_600,
                                            ),
                                            ft.Text(
                                                f"Iznajmljeno: {format_date(loan['loan_date'])}",
                                                size=12,
                                                color=ft.Colors.GREY_500,
                                            ),
                                        ],
                                        expand=True,
                                    ),
                                    ft.Column(
                                        [item for item in [
                                            ft.Text(
                                                get_status_text(loan["status"]),
                                                size=12,
                                                color=get_status_color(loan["status"]),
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(
                                                f"Vraćanje: {format_date(loan['due_date'])}",
                                                size=10,
                                                color=ft.Colors.GREY_500,
                                            ),

                                        ] if item is not None],
                                        horizontal_alignment=ft.CrossAxisAlignment.END,
                                    ),
                                ],
                                spacing=16,
                            ),
                            ft.Row(
                                [button for button in [
                                    ft.TextButton(
                                        "Produži",
                                        icon=ft.Icons.REFRESH,
                                        on_click=lambda l=loan: renew_loan(l["id"]),
                                    ) if loan["status"] == "active" else None,
                                    ft.TextButton(
                                        "Vrati",
                                        icon=ft.Icons.CHECK_CIRCLE,
                                        on_click=lambda l=loan: return_book(l["id"]),
                                    ) if loan["status"] == "active" else None,

                                ] if button is not None],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ],
                        spacing=12,
                    ),
                    padding=16,
                ),
            ) for loan in loans
        ]
        
        loans_list = ft.Column(loans_content, spacing=16)
    else:
        loans_list = ft.Column([
            ft.Text(
                "Moje iznajmljene knjige",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_900,
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.BOOK, size=48, color=ft.Colors.GREY_400),
                        ft.Text(
                            "Nemate iznajmljenih knjiga",
                            size=16,
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=40,
                ),
            ),
        ], spacing=16)
    
    # Summary card
    active_loans = len([loan for loan in loans if loan["status"] == "active"])


    
    summary_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Pregled",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),
                    ft.Divider(height=16),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        str(active_loans),
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.GREEN,
                                    ),
                                    ft.Text(
                                        "Aktivne knjige",
                                        size=12,
                                        color=ft.Colors.GREY_600,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
    
    # Main content
    content = ft.Column(
        [
            summary_card,
            ft.Divider(height=32),
            loans_list,
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
