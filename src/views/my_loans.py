import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import show_snack_bar
from datetime import datetime, timedelta
from utils.session_manager import get_current_user
from controllers.admin_controller import get_all_loans, return_loan

def my_loans(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Moje iznajmljene knjige - Biblioteka"
    
    # Navigation bar
    navbar_content = NavBar("member", page_data)
    
    # Get current user and loans from database
    current_user = get_current_user()
    all_loans = get_all_loans()
    
    # Filter loans for current user
    user_id = current_user.get("id")
    loans = [loan for loan in all_loans if loan.get("member_id") == user_id]
    
    # If no loans found, show empty state
    if not loans:
        loans = []
    
    def renew_loan(loan_id):
        """Renew a loan - extend the due date by 14 days"""
        from datetime import datetime, timedelta
        
        # Find the loan and extend it
        loan_found = False
        
        for i, loan in enumerate(all_loans):
            if loan.get('id') == loan_id and loan.get('status') == 'active':
                # Calculate new due date
                current_due_date = datetime.strptime(loan.get('due_date'), "%Y-%m-%d")
                new_due_date = current_due_date + timedelta(days=14)
                
                # Update the loan in the database
                from controllers.admin_controller import update_loan
                success, message = update_loan(loan_id, new_due_date.strftime("%Y-%m-%d"))
                
                if success:
                    show_snack_bar(page, "Knjiga je uspešno produžena za 14 dana!", "SUCCESS")
                    # Refresh the page
                    page_data.navigate('my_loans')
                else:
                    show_snack_bar(page, f"Greška: {message}", "ERROR")
                return
        
        if not loan_found:
            show_snack_bar(page, "Pozajmica nije pronađena ili je već vraćena!", "ERROR")
    
    def return_book(loan_id):
        """Return a book - mark loan as returned and update book availability"""
        try:
            # Use the database function to return the loan
            success, message = return_loan(loan_id)
            
            if success:
                show_snack_bar(page, "Knjiga je uspešno vraćena!", "SUCCESS")
                # Refresh the page by re-navigating
                page_data.navigate('my_loans')
            else:
                show_snack_bar(page, f"Greška: {message}", "ERROR")
            
        except Exception as e:
            show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
    

    
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
    
    # Create list of all controls for ListView
    all_controls = [
        summary_card,
        ft.Divider(height=32),
    ]
    
    # Add loans content directly to ListView (not as nested Column)
    if loans:
        all_controls.append(
            ft.Text(
                "Moje iznajmljene knjige",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_900,
            )
        )
        # Add each loan card directly
        for loan in loans:
            loan_card = ft.Card(
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
                                        on_click=lambda e, l=loan: renew_loan(l["id"]),
                                    ) if loan["status"] == "active" else None,
                                    ft.TextButton(
                                        "Vrati",
                                        icon=ft.Icons.CHECK_CIRCLE,
                                        on_click=lambda e, l=loan: return_book(l["id"]),
                                    ) if loan["status"] == "active" else None,
                                ] if button is not None],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ],
                        spacing=12,
                    ),
                    padding=16,
                ),
            )
            all_controls.append(loan_card)
    else:
        all_controls.extend([
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
            )
        ])
    
    # Add bottom spacing
    all_controls.append(ft.Container(height=50))
    
    # Main content with ListView for proper scrolling (like dashboard)
    content = ft.ListView(
        controls=all_controls,
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
