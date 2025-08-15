import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import SnackBar
from utils.global_state import global_state

def admin_books(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Upravljanje knjigama - Biblioteka"
    
    # Navigation bar
    navbar_content = NavBar("admin", page_data)
    
    # Get books from global state or initialize with sample data
    books = global_state.get("books", [])
    
    # If no books exist, initialize with sample data
    if not books:
        books = [
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
                "isbn": "978-86-7436-130-3",
                "category": "Roman",
                "publication_year": 1957,
                "publisher": "Laguna",
                "total_copies": 2,
                "available_copies": 0,
                "location": "Polica A-22",
                "status": "unavailable"
            }
        ]
        global_state.set("books", books)
    
    # Books list
    books_list = ft.Column(
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    
    def update_books_list(books_to_show):
        books_list.controls.clear()
        
        for book in books_to_show:
            book_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.BOOK,
                                        color=ft.Colors.BLUE if book['status'] == 'available' else ft.Colors.GREY,
                                        size=24,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(
                                                book['title'],
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(
                                                f"Autor: {book['author']}",
                                                size=14,
                                                color=ft.Colors.GREY_600,
                                            ),
                                            ft.Text(
                                                f"ISBN: {book['isbn']} | Kategorija: {book['category']}",
                                                size=12,
                                                color=ft.Colors.GREY_500,
                                            ),
                                            ft.Text(
                                                f"Primerci: {book['available_copies']}/{book['total_copies']} | Lokacija: {book['location']}",
                                                size=12,
                                                color=ft.Colors.GREY_500,
                                            ),
                                        ],
                                        expand=True,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(
                                                "Dostupno" if book['status'] == 'available' else "Nedostupno",
                                                size=12,
                                                color=ft.Colors.GREEN if book['status'] == 'available' else ft.Colors.RED,
                                                weight=ft.FontWeight.BOLD,
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
                                         "Uredi",
                                         icon=ft.Icons.EDIT,
                                         on_click=lambda e, b=book: edit_book(b),
                                     ),
                                     ft.TextButton(
                                         "Obriši",
                                         icon=ft.Icons.DELETE,
                                         on_click=lambda e, b=book: delete_book(b),
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
            books_list.controls.append(book_card)
        
        page.update()
    
    def close_dialog():
        page.dialog.open = False
        page.update()
    
    def add_book(e):
        # Show add book dialog
        page.dialog = ft.AlertDialog(
            title=ft.Text("Dodaj novu knjigu"),
            content=ft.Column(
                [
                    ft.TextField(label="Naslov"),
                    ft.TextField(label="Autor"),
                    ft.TextField(label="ISBN"),
                    ft.Dropdown(
                        label="Kategorija",
                        options=[
                            ft.dropdown.Option("Roman"),
                            ft.dropdown.Option("Naučna fantastika"),
                            ft.dropdown.Option("Detektivski"),
                            ft.dropdown.Option("Istorijski"),
                            ft.dropdown.Option("Naučna literatura"),
                        ],
                    ),
                    ft.TextField(label="Godina izdanja", keyboard_type=ft.KeyboardType.NUMBER),
                    ft.TextField(label="Izdavač"),
                    ft.TextField(label="Broj primeraka", keyboard_type=ft.KeyboardType.NUMBER),
                    ft.TextField(label="Lokacija"),
                ],
                spacing=8,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("Otkaži", on_click=lambda _: close_dialog()),
                ft.TextButton("Dodaj", on_click=lambda _: save_book()),
            ],
        )
        page.dialog.open = True
        page.update()
    
    def save_book():
        # Get form data from dialog
        dialog_content = page.dialog.content
        form_fields = dialog_content.controls
        
        # Extract values from form fields
        title = form_fields[0].value
        author = form_fields[1].value
        isbn = form_fields[2].value
        category = form_fields[3].value
        year = form_fields[4].value
        publisher = form_fields[5].value
        copies = form_fields[6].value
        location = form_fields[7].value
        
        # Validate required fields
        if not title or not author or not isbn:
            page.overlay.append(
                SnackBar("Molimo popunite sva obavezna polja!", duration=3000)
            )
            page.update()
            return
        
        # Create new book
        new_book = {
            "id": len(books) + 1,
            "title": title,
            "author": author,
            "isbn": isbn,
            "category": category or "Roman",
            "publication_year": int(year) if year else 2024,
            "publisher": publisher or "Nepoznato",
            "total_copies": int(copies) if copies else 1,
            "available_copies": int(copies) if copies else 1,
            "location": location or "Nepoznato",
            "status": "available"
        }
        
        # Add to books list
        books.append(new_book)
        
        # Save to global state
        global_state.set("books", books)
        
        # Update the display
        update_books_list(books)
        
        # Show success message
        page.overlay.append(
            SnackBar("Knjiga je uspešno dodana!", duration=3000)
        )
        close_dialog()
        page.update()
    
    def edit_book(book):
        # Show edit book dialog
        page.dialog = ft.AlertDialog(
            title=ft.Text(f"Uredi knjigu: {book['title']}"),
            content=ft.Column(
                [
                    ft.TextField(label="Naslov", value=book['title']),
                    ft.TextField(label="Autor", value=book['author']),
                    ft.TextField(label="ISBN", value=book['isbn']),
                    ft.Dropdown(
                        label="Kategorija",
                        value=book['category'],
                        options=[
                            ft.dropdown.Option("Roman"),
                            ft.dropdown.Option("Naučna fantastika"),
                            ft.dropdown.Option("Detektivski"),
                            ft.dropdown.Option("Istorijski"),
                            ft.dropdown.Option("Naučna literatura"),
                        ],
                    ),
                    ft.TextField(label="Godina izdanja", value=str(book['publication_year'])),
                    ft.TextField(label="Izdavač", value=book['publisher']),
                    ft.TextField(label="Broj primeraka", value=str(book['total_copies'])),
                    ft.TextField(label="Lokacija", value=book['location']),
                ],
                spacing=8,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("Otkaži", on_click=lambda _: close_dialog()),
                ft.TextButton("Sačuvaj", on_click=lambda _: update_book(book['id'])),
            ],
        )
        page.dialog.open = True
        page.update()
    
    def update_book(book_id):
        # Get form data from dialog
        dialog_content = page.dialog.content
        form_fields = dialog_content.controls
        
        # Extract values from form fields
        title = form_fields[0].value
        author = form_fields[1].value
        isbn = form_fields[2].value
        category = form_fields[3].value
        year = form_fields[4].value
        publisher = form_fields[5].value
        copies = form_fields[6].value
        location = form_fields[7].value
        
        # Validate required fields
        if not title or not author or not isbn:
            page.overlay.append(
                SnackBar("Molimo popunite sva obavezna polja!", duration=3000)
            )
            page.update()
            return
        
        # Find and update the book
        for book in books:
            if book['id'] == book_id:
                book['title'] = title
                book['author'] = author
                book['isbn'] = isbn
                book['category'] = category or book['category']
                book['publication_year'] = int(year) if year else book['publication_year']
                book['publisher'] = publisher or book['publisher']
                book['total_copies'] = int(copies) if copies else book['total_copies']
                book['location'] = location or book['location']
                break
        
        # Save to global state
        global_state.set("books", books)
        
        # Update the display
        update_books_list(books)
        
        # Show success message
        page.overlay.append(
            SnackBar("Knjiga je uspešno ažurirana!", duration=3000)
        )
        close_dialog()
        page.update()
    
    def delete_book(book):
        # Show confirmation dialog
        page.dialog = ft.AlertDialog(
            title=ft.Text("Potvrda brisanja"),
            content=ft.Text(f"Da li ste sigurni da želite da obrišete knjigu '{book['title']}'?"),
            actions=[
                ft.TextButton("Otkaži", on_click=lambda _: close_dialog()),
                ft.TextButton("Obriši", on_click=lambda _: confirm_delete(book['id'])),
            ],
        )
        page.dialog.open = True
        page.update()
    
    def confirm_delete(book_id):
        # Remove book from list
        books[:] = [book for book in books if book['id'] != book_id]
        
        # Save to global state
        global_state.set("books", books)
        
        # Update the display
        update_books_list(books)
        
        # Show success message
        page.overlay.append(
            SnackBar("Knjiga je uspešno obrisana!", duration=3000)
        )
        close_dialog()
        page.update()
    
    def search_books(e):
        query = search_tf.value.lower()
        # Filter books based on search query
        filtered_books = [book for book in books if 
                         query in book['title'].lower() or 
                         query in book['author'].lower() or 
                         query in book['isbn']]
        update_books_list(filtered_books)
    
    # Search input (defined after all functions)
    search_tf = ft.TextField(
        label="Pretraži knjige...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        on_submit=search_books,
    )
    
    search_button = ft.ElevatedButton(
        "Pretraži",
        icon=ft.Icons.SEARCH,
        on_click=search_books,
    )
    
    # Initialize books list
    update_books_list(books)
    
    # Main content
    content = ft.Column(
        [
            ft.Row(
                [
                    ft.Text(
                        "Upravljanje knjigama",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),
                    ft.ElevatedButton(
                        "Dodaj knjigu",
                        icon=ft.Icons.ADD,
                        on_click=add_book,
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
                content=books_list,
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
