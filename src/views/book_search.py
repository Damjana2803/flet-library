import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import SnackBar

def book_search(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Pretraga knjiga - Biblioteka"
    
    # Navigation bar
    navbar_content = NavBar("member", page_data)
    
    # Search results
    search_results = []
    
    def on_search(e):
        query = search_tf.value.strip()
        
        # Get all books from global state
        from utils.global_state import global_state
        all_books = global_state.get("books", [])
        
        # If no books exist, initialize with sample data
        if not all_books:
            all_books = [
                {
                    "id": 1,
                    "title": "Rat i mir",
                    "author": "Lav Tolstoj",
                    "isbn": "978-86-7436-123-4",
                    "category": "Roman",
                    "publication_year": 1869,
                    "publisher": "Laguna",
                    "total_copies": 5,
                    "available_copies": 3,
                    "location": "Polica A-15",
                    "status": "available"
                },
                {
                    "id": 2,
                    "title": "Ana Karenjina",
                    "author": "Lav Tolstoj",
                    "isbn": "978-86-7436-124-1",
                    "category": "Roman",
                    "publication_year": 1877,
                    "publisher": "Laguna",
                    "total_copies": 3,
                    "available_copies": 0,
                    "location": "Polica A-16",
                    "status": "unavailable"
                },
                {
                    "id": 3,
                    "title": "Zločin i kazna",
                    "author": "Fjodor Dostojevski",
                    "isbn": "978-86-7436-125-8",
                    "category": "Roman",
                    "publication_year": 1866,
                    "publisher": "Laguna",
                    "total_copies": 4,
                    "available_copies": 2,
                    "location": "Polica A-17",
                    "status": "available"
                },
                {
                    "id": 4,
                    "title": "Braća Karamazovi",
                    "author": "Fjodor Dostojevski",
                    "isbn": "978-86-7436-126-5",
                    "category": "Roman",
                    "publication_year": 1880,
                    "publisher": "Laguna",
                    "total_copies": 3,
                    "available_copies": 1,
                    "location": "Polica A-18",
                    "status": "available"
                },
                {
                    "id": 5,
                    "title": "Idiot",
                    "author": "Fjodor Dostojevski",
                    "isbn": "978-86-7436-127-2",
                    "category": "Roman",
                    "publication_year": 1869,
                    "publisher": "Laguna",
                    "total_copies": 2,
                    "available_copies": 0,
                    "location": "Polica A-19",
                    "status": "unavailable"
                },
                {
                    "id": 6,
                    "title": "Evgenij Onjegin",
                    "author": "Aleksandar Puškin",
                    "isbn": "978-86-7436-128-9",
                    "category": "Roman",
                    "publication_year": 1833,
                    "publisher": "Laguna",
                    "total_copies": 4,
                    "available_copies": 2,
                    "location": "Polica A-20",
                    "status": "available"
                },
                {
                    "id": 7,
                    "title": "Majstor i Margarita",
                    "author": "Mihail Bulgakov",
                    "isbn": "978-86-7436-129-6",
                    "category": "Roman",
                    "publication_year": 1967,
                    "publisher": "Laguna",
                    "total_copies": 3,
                    "available_copies": 1,
                    "location": "Polica A-21",
                    "status": "available"
                },
                {
                    "id": 8,
                    "title": "Doktor Živago",
                    "author": "Boris Pasternak",
                    "isbn": "978-86-7436-130-2",
                    "category": "Roman",
                    "publication_year": 1957,
                    "publisher": "Laguna",
                    "total_copies": 2,
                    "available_copies": 0,
                    "location": "Polica A-22",
                    "status": "unavailable"
                }
            ]
            global_state.set("books", all_books)
        
        # Filter books based on search query
        if query:
            filtered_books = []
            query_lower = query.lower()
            for book in all_books:
                if (query_lower in book.get("title", "").lower() or
                    query_lower in book.get("author", "").lower() or
                    query_lower in book.get("isbn", "").lower() or
                    query_lower in book.get("category", "").lower()):
                    filtered_books.append(book)
            search_results.clear()
            search_results.extend(filtered_books)
        else:
            # Show all books if no search query
            search_results.clear()
            search_results.extend(all_books)
        
        update_search_results()
    
    def update_search_results():
        results_column.content.controls.clear()
        
        if not search_results:
            results_column.content.controls.append(
                ft.Text(
                    "Unesite pojam za pretragu ili nema rezultata",
                    size=16,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                )
            )
        else:
            for book in search_results:
                book_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                                                                 ft.Icon(
                                             ft.Icons.BOOK,
                                             color=ft.Colors.BLUE if book.get("available_copies", 0) > 0 else ft.Colors.GREY,
                                             size=24,
                                         ),
                                        ft.Column(
                                            [
                                                ft.Text(
                                                    book["title"],
                                                    size=18,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                                ft.Text(
                                                    f"Autor: {book['author']}",
                                                    size=14,
                                                    color=ft.Colors.GREY_600,
                                                ),
                                                                                                 ft.Text(
                                                     f"Kategorija: {book['category']} ({book['publication_year']})",
                                                     size=12,
                                                     color=ft.Colors.GREY_500,
                                                 ),
                                            ],
                                            expand=True,
                                        ),
                                        ft.Column(
                                            [
                                                                                                 ft.Text(
                                                     "Dostupno" if book.get("available_copies", 0) > 0 else "Nedostupno",
                                                     size=12,
                                                     color=ft.Colors.GREEN if book.get("available_copies", 0) > 0 else ft.Colors.RED,
                                                     weight=ft.FontWeight.BOLD,
                                                 ),
                                                ft.Text(
                                                    book["location"],
                                                    size=10,
                                                    color=ft.Colors.GREY_500,
                                                ),
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.END,
                                        ),
                                    ],
                                    spacing=16,
                                ),
                                ft.Row(
                                    [
                                                                                 ft.TextButton(
                                             "Rezerviši" if book.get("available_copies", 0) == 0 else "Iznajmi",
                                             icon=ft.Icons.BOOKMARK if book.get("available_copies", 0) == 0 else ft.Icons.LIBRARY_BOOKS,
                                             on_click=lambda e, b=book: on_book_action(b),
                                         ),
                                        ft.TextButton(
                                            "Detalji",
                                            icon=ft.Icons.INFO,
                                            on_click=lambda e, b=book: show_book_details(b),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                            ],
                            spacing=12,
                        ),
                        padding=16,
                    ),
                )
                results_column.content.controls.append(book_card)
        
        page.update()
    
    def on_book_action(book):
        if book.get("available_copies", 0) > 0:
            # Borrow book
            borrow_book(book)
        else:
            # Reserve book
            page.overlay.append(
                SnackBar(
                    f"Knjiga '{book['title']}' je rezervisana!",
                    duration=3000
                )
            )
        page.update()
    
    def borrow_book(book):
        """Borrow a book - create a new loan"""
        from utils.global_state import global_state
        from datetime import datetime, timedelta
        
        # Get current user
        current_user = global_state.get("user", {})
        if not current_user:
            page.overlay.append(
                SnackBar("Morate biti prijavljeni da iznajmite knjigu!", duration=3000)
            )
            page.update()
            return
        
        # Check if user can borrow more books
        current_loans = current_user.get('current_loans', 0)
        max_loans = current_user.get('max_loans', 5)
        
        if current_loans >= max_loans:
            page.overlay.append(
                SnackBar(f"Možete iznajmiti maksimalno {max_loans} knjiga!", duration=3000)
            )
            page.update()
            return
        
        # Get all books and loans
        all_books = global_state.get("books", [])
        all_loans = global_state.get("loans", [])
        
        # Find the book and update its availability
        book_found = False
        for i, b in enumerate(all_books):
            if b.get('id') == book.get('id'):
                if b.get('available_copies', 0) > 0:
                    all_books[i]['available_copies'] = b.get('available_copies', 0) - 1
                    book_found = True
                    break
                else:
                    page.overlay.append(
                        SnackBar("Knjiga nije dostupna!", duration=3000)
                    )
                    page.update()
                    return
        
        if not book_found:
            page.overlay.append(
                SnackBar("Knjiga nije pronađena!", duration=3000)
            )
            page.update()
            return
        
        # Create new loan
        loan_date = datetime.now()
        due_date = loan_date + timedelta(days=14)  # 14 days loan period
        
        new_loan = {
            'id': len(all_loans) + 1,
            'book_id': book.get('id'),
            'book_title': book.get('title'),
            'book_author': book.get('author'),
            'member_id': current_user.get('id'),
            'member_name': f"{current_user.get('first_name', '')} {current_user.get('last_name', '')}",
            'loan_date': loan_date.strftime("%Y-%m-%d"),
            'due_date': due_date.strftime("%Y-%m-%d"),
            'status': 'active',
            'returned_date': None
        }
        
        # Add loan to global state
        all_loans.append(new_loan)
        
        # Update user's current loans count
        current_user['current_loans'] = current_loans + 1
        
        # Save to global state
        global_state.set("books", all_books)
        global_state.set("loans", all_loans)
        global_state.set("user", current_user)
        
        # Show success message
        page.overlay.append(
            SnackBar(
                f"Knjiga '{book['title']}' je uspešno iznajmljena! Vraćanje: {due_date.strftime('%d.%m.%Y')}",
                duration=4000
            )
        )
        page.update()
    
    def show_book_details(book):
        # Show book details modal
        page.dialog = ft.AlertDialog(
            title=ft.Text(book["title"]),
            content=ft.Column(
                [
                    ft.Text(f"Autor: {book['author']}"),
                    ft.Text(f"ISBN: {book['isbn']}"),
                    ft.Text(f"Kategorija: {book['category']}"),
                                         ft.Text(f"Godina: {book['publication_year']}"),
                    ft.Text(f"Lokacija: {book['location']}"),
                                         ft.Text(
                         f"Status: {'Dostupno' if book.get('available_copies', 0) > 0 else 'Nedostupno'}",
                         color=ft.Colors.GREEN if book.get('available_copies', 0) > 0 else ft.Colors.RED,
                         weight=ft.FontWeight.BOLD,
                     ),
                ],
                spacing=8,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("Zatvori", on_click=lambda _: close_dialog()),
            ],
        )
        page.dialog.open = True
        page.update()
    
    def close_dialog():
        page.dialog.open = False
        page.update()
    
    # Search input
    search_tf = ft.TextField(
        label="Pretraži knjige...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        on_submit=on_search,
    )
    
    search_button = ft.ElevatedButton(
        "Pretraži",
        icon=ft.Icons.SEARCH,
        on_click=on_search,
    )
    
    # Filters
    category_dropdown = ft.Dropdown(
        label="Kategorija",
        options=[
            ft.dropdown.Option("Sve kategorije"),
            ft.dropdown.Option("Roman"),
            ft.dropdown.Option("Naučna fantastika"),
            ft.dropdown.Option("Detektivski"),
            ft.dropdown.Option("Istorijski"),
            ft.dropdown.Option("Naučna literatura"),
        ],
        width=200,
    )
    
    availability_dropdown = ft.Dropdown(
        label="Dostupnost",
        options=[
            ft.dropdown.Option("Sve"),
            ft.dropdown.Option("Dostupno"),
            ft.dropdown.Option("Nedostupno"),
        ],
        width=200,
    )
    
    # Results column
    results_column = ft.Container(
        content=ft.Column(
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        ),
        height=500,  # Fixed height to enable scrolling
        expand=True,
    )
    
    # Main content
    content = ft.Column(
        [
            ft.Text(
                "Pretraga knjiga",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_900,
            ),
            ft.Row(
                [search_tf, search_button],
                spacing=16,
            ),
            ft.Row(
                [category_dropdown, availability_dropdown],
                spacing=16,
            ),
            ft.Divider(height=32),
            ft.Text(
                "Rezultati pretrage",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_900,
            ),
            results_column,
        ],
        spacing=16,
        expand=True,
    )
    
    # Load all books when page opens
    on_search(None)
    
    return ft.Column([
        navbar_content,
        ft.Container(
            content=content,
            padding=20,
            expand=True,

        )
    ])
