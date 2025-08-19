import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import show_snack_bar
from controllers.admin_controller import add_book, get_all_books, delete_book, update_book
from utils.global_state import global_state

def admin_books(page_data: PageData):
    page = page_data.page
    page.title = "Upravljanje knjigama - Biblioteka"
    
    # Check if mobile screen
    is_mobile = page.width < 768 if page.width else False
    
    # State variables
    books = []
    search_query = ft.TextField(
        label="Pretraži knjige",
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: filter_books()
    )
    
    # Dialog fields for adding new book
    title_field = ft.TextField(label="Naslov *", hint_text="Unesite naslov knjige")
    author_field = ft.TextField(label="Autor *", hint_text="Unesite ime autora")
    isbn_field = ft.TextField(label="ISBN *", hint_text="Unesite ISBN broj")
    category_field = ft.TextField(label="Kategorija", hint_text="Unesite kategoriju")
    year_field = ft.TextField(label="Godina izdanja *", hint_text="Unesite godinu")
    publisher_field = ft.TextField(label="Izdavač", hint_text="Unesite izdavača")
    description_field = ft.TextField(label="Opis", multiline=True, min_lines=3, max_lines=5, hint_text="Unesite opis knjige")
    copies_field = ft.TextField(label="Broj primeraka *", hint_text="Unesite broj primeraka")
    location_field = ft.TextField(label="Lokacija", hint_text="Unesite lokaciju")
    
    # Add book dialog
    add_dialog = ft.AlertDialog(
        title=ft.Text("Dodaj novu knjigu"),
        content=ft.Column([
            title_field,
            author_field,
            isbn_field,
            category_field,
            year_field,
            publisher_field,
            description_field,
            copies_field,
            location_field
        ], scroll=ft.ScrollMode.AUTO, height=400),
        actions=[
            ft.TextButton("Otkaži", on_click=lambda e: close_add_dialog()),
            ft.TextButton("Dodaj", on_click=lambda e: save_book())
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    # Edit book dialog fields
    edit_title_field = ft.TextField(label="Naslov *", hint_text="Unesite naslov knjige")
    edit_author_field = ft.TextField(label="Autor *", hint_text="Unesite ime autora")
    edit_isbn_field = ft.TextField(label="ISBN *", hint_text="Unesite ISBN broj")
    edit_category_field = ft.TextField(label="Kategorija", hint_text="Unesite kategoriju")
    edit_year_field = ft.TextField(label="Godina izdanja *", hint_text="Unesite godinu")
    edit_publisher_field = ft.TextField(label="Izdavač", hint_text="Unesite izdavača")
    edit_description_field = ft.TextField(label="Opis", multiline=True, min_lines=3, max_lines=5, hint_text="Unesite opis knjige")
    edit_copies_field = ft.TextField(label="Broj primeraka *", hint_text="Unesite broj primeraka")
    edit_location_field = ft.TextField(label="Lokacija", hint_text="Unesite lokaciju")
    
    # Edit book dialog
    edit_dialog = ft.AlertDialog(
        title=ft.Text("Izmeni knjigu"),
        content=ft.Column([
            edit_title_field,
            edit_author_field,
            edit_isbn_field,
            edit_category_field,
            edit_year_field,
            edit_publisher_field,
            edit_description_field,
            edit_copies_field,
            edit_location_field
        ], scroll=ft.ScrollMode.AUTO, height=400),
        actions=[
            ft.TextButton("Otkaži", on_click=lambda e: close_edit_dialog()),
            ft.TextButton("Sačuvaj", on_click=lambda e: update_book_action())
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    def open_add_dialog():
        page.dialog = add_dialog
        add_dialog.open = True
        page.update()
    
    def close_add_dialog():
        add_dialog.open = False
        page.update()
    
    def open_edit_dialog(book_data):
        # Prepopulate fields with book data
        edit_title_field.value = book_data.get('title', '')
        edit_author_field.value = book_data.get('author', '')
        edit_isbn_field.value = book_data.get('isbn', '')
        edit_category_field.value = book_data.get('category', '')
        edit_year_field.value = str(book_data.get('publication_year', ''))
        edit_publisher_field.value = book_data.get('publisher', '')
        edit_description_field.value = book_data.get('description', '')
        edit_copies_field.value = str(book_data.get('total_copies', ''))
        edit_location_field.value = book_data.get('location', '')
        
        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()
    
    def close_edit_dialog():
        edit_dialog.open = False
        page.update()
    
    def save_book():
        try:
            # Validate required fields
            if not title_field.value or not author_field.value or not isbn_field.value:
                show_snack_bar(page, "Molimo popunite sva obavezna polja", "ERROR")
                return
            
            # Convert year to int (remove any trailing dots or spaces)
            try:
                year_str = year_field.value.strip().rstrip('.')
                year = int(year_str)
            except ValueError:
                show_snack_bar(page, "Godina izdanja mora biti broj", "ERROR")
                return
            
            # Convert copies to int (remove any trailing dots or spaces)
            try:
                copies_str = copies_field.value.strip().rstrip('.')
                copies = int(copies_str)
            except ValueError:
                show_snack_bar(page, "Broj primeraka mora biti broj", "ERROR")
                return
            
            # Add book
            success, message = add_book(
                title=title_field.value,
                author=author_field.value,
                isbn=isbn_field.value,
                category=category_field.value or "Opšta",
                publication_year=year,
                publisher=publisher_field.value or "Nepoznato",
                description=description_field.value or "",
                total_copies=copies,
                location=location_field.value or "Glavna biblioteka"
            )
            
            if success:
                show_snack_bar(page, "Knjiga uspešno dodata!", "SUCCESS")
                close_add_dialog()
                clear_dialog_fields()
                load_books()  # Refresh the list
            else:
                show_snack_bar(page, f"Greška: {message}", "ERROR")
                
        except Exception as e:
            show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
    
    # Variable to store book being edited
    current_editing_book_id = None
    
    def update_book_action():
        try:
            # Validate required fields
            if not edit_title_field.value or not edit_author_field.value or not edit_isbn_field.value:
                show_snack_bar(page, "Molimo popunite sva obavezna polja", "ERROR")
                return
            
            # Convert year to int (remove any trailing dots or spaces)
            try:
                year_str = edit_year_field.value.strip().rstrip('.')
                year = int(year_str)
            except ValueError:
                show_snack_bar(page, "Godina izdanja mora biti broj", "ERROR")
                return
            
            # Convert copies to int (remove any trailing dots or spaces)
            try:
                copies_str = edit_copies_field.value.strip().rstrip('.')
                copies = int(copies_str)
            except ValueError:
                show_snack_bar(page, "Broj primeraka mora biti broj", "ERROR")
                return
            
            # Update book
            success, message = update_book(
                book_id=current_editing_book_id,
                title=edit_title_field.value,
                author=edit_author_field.value,
                isbn=edit_isbn_field.value,
                category=edit_category_field.value or "Opšta",
                publication_year=year,
                publisher=edit_publisher_field.value or "Nepoznato",
                description=edit_description_field.value or "",
                total_copies=copies,
                location=edit_location_field.value or "Glavna biblioteka"
            )
            
            if success:
                show_snack_bar(page, "Knjiga uspešno ažurirana!", "SUCCESS")
                close_edit_dialog()
                clear_edit_dialog_fields()
                load_books()  # Refresh the list
            else:
                show_snack_bar(page, f"Greška: {message}", "ERROR")
                
        except Exception as e:
            show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
    
    def clear_dialog_fields():
        title_field.value = ""
        author_field.value = ""
        isbn_field.value = ""
        category_field.value = ""
        year_field.value = ""
        publisher_field.value = ""
        description_field.value = ""
        copies_field.value = ""
        location_field.value = ""
        page.update()
    
    def clear_edit_dialog_fields():
        edit_title_field.value = ""
        edit_author_field.value = ""
        edit_isbn_field.value = ""
        edit_category_field.value = ""
        edit_year_field.value = ""
        edit_publisher_field.value = ""
        edit_description_field.value = ""
        edit_copies_field.value = ""
        edit_location_field.value = ""
        page.update()
    
    def load_books():
        try:
            all_books = get_all_books()
            books.clear()
            books.extend(all_books)
            
            # If no books exist, add some sample data
            if not books:
                sample_books = [
                    {
                        'id': 1,
                        'title': 'Prvi korak u programiranju',
                        'author': 'Marko Petrović',
                        'isbn': '978-86-123-4567-8',
                        'category': 'Programiranje',
                        'publication_year': 2023,
                        'publisher': 'Tehnička knjiga',
                        'description': 'Uvod u programiranje za početnike',
                        'total_copies': 5,
                        'available_copies': 5,
                        'location': 'Glavna biblioteka',
                        'status': 'available'
                    },
                    {
                        'id': 2,
                        'title': 'Baze podataka',
                        'author': 'Ana Jovanović',
                        'isbn': '978-86-234-5678-9',
                        'category': 'Baze podataka',
                        'publication_year': 2022,
                        'publisher': 'Fakultet organizacionih nauka',
                        'description': 'Teorija i praksa baza podataka',
                        'total_copies': 3,
                        'available_copies': 2,
                        'location': 'Glavna biblioteka',
                        'status': 'available'
                    }
                ]
                books.extend(sample_books)
            
            update_books_table()
        except Exception as e:
            print(f"Greška pri učitavanju knjiga: {str(e)}")
            # Add sample data if there's an error
            sample_books = [
                {
                    'id': 1,
                    'title': 'Prvi korak u programiranju',
                    'author': 'Marko Petrović',
                    'isbn': '978-86-123-4567-8',
                    'category': 'Programiranje',
                    'publication_year': 2023,
                    'publisher': 'Tehnička knjiga',
                    'description': 'Uvod u programiranje za početnike',
                    'total_copies': 5,
                    'available_copies': 5,
                    'location': 'Glavna biblioteka',
                    'status': 'available'
                },
                {
                    'id': 2,
                    'title': 'Baze podataka',
                    'author': 'Ana Jovanović',
                    'isbn': '978-86-234-5678-9',
                    'category': 'Baze podataka',
                    'publication_year': 2022,
                    'publisher': 'Fakultet organizacionih nauka',
                    'description': 'Teorija i praksa baza podataka',
                    'total_copies': 3,
                    'available_copies': 2,
                    'location': 'Glavna biblioteka',
                    'status': 'available'
                }
            ]
            books.extend(sample_books)
            update_books_table()
    
    def filter_books():
        query = search_query.value.lower()
        if not query:
            load_books()
            return
        
        filtered_books = [book for book in books if 
                         query in book.get('title', '').lower() or
                         query in book.get('author', '').lower() or
                         query in book.get('isbn', '').lower()]
        update_books_table(filtered_books)
    
    def update_books_table(books_to_show=None):
        if books_to_show is None:
            books_to_show = books
        
        # Mobile: use cards instead of table, Desktop: use DataTable
        if is_mobile:
            update_books_cards(books_to_show)
        else:
            update_books_datatable(books_to_show)
    
    def update_books_cards(books_to_show):
        """Mobile-friendly card layout"""
        books_container.controls.clear()
        
        for book in books_to_show:
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(book.get('title', ''), size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Autor: {book.get('author', '')}", size=14),
                        ft.Text(f"ISBN: {book.get('isbn', '')}", size=12, color=ft.Colors.GREY_600),
                        ft.Text(f"Kategorija: {book.get('category', '')}", size=12),
                        ft.Text(f"Kopije: {book.get('available_copies', 0)}/{book.get('total_copies', 0)}", size=12),
                        ft.Row([
                            ft.ElevatedButton(
                                text="Izmeni",
                                icon=ft.Icons.EDIT,
                                on_click=lambda e, book_id=book.get('id'): edit_book(book_id),
                                expand=True
                            ),
                            ft.ElevatedButton(
                                text="Obriši",
                                icon=ft.Icons.DELETE,
                                style=ft.ButtonStyle(color=ft.Colors.RED),
                                on_click=lambda e, book_id=book.get('id'): delete_book_confirm(book_id),
                                expand=True
                            )
                        ], spacing=10)
                    ], spacing=8),
                    padding=15
                )
            )
            books_container.controls.append(card)
        
        page.update()
    
    def update_books_datatable(books_to_show):
        """Desktop DataTable layout"""
        table_rows = []
        for book in books_to_show:
            table_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(book.get('title', ''))),
                        ft.DataCell(ft.Text(book.get('author', ''))),
                        ft.DataCell(ft.Text(book.get('isbn', ''))),
                        ft.DataCell(ft.Text(book.get('category', ''))),
                        ft.DataCell(ft.Text(str(book.get('total_copies', 0)))),
                        ft.DataCell(ft.Text(book.get('location', ''))),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color=ft.Colors.BLUE,
                                    tooltip="Izmeni",
                                    on_click=lambda e, book_id=book.get('id'): edit_book(book_id)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.RED,
                                    tooltip="Obriši",
                                    on_click=lambda e, book_id=book.get('id'): delete_book_confirm(book_id)
                                )
                            ])
                        )
                    ]
                )
            )
        
        books_table.rows = table_rows
        page.update()
    
    def edit_book(book_id):
        nonlocal current_editing_book_id
        current_editing_book_id = book_id
        
        # Find the book data
        book_data = None
        for book in books:
            if book.get('id') == book_id:
                book_data = book
                break
        
        if book_data:
            open_edit_dialog(book_data)
        else:
            show_snack_bar(page, "Knjiga nije pronađena", "ERROR")
    
    def delete_book_confirm(book_id):
        def confirm_delete(e):
            try:
                success, message = delete_book(book_id)
                if success:
                    show_snack_bar(page, "Knjiga uspešno obrisana!", "SUCCESS")
                    load_books()
                else:
                    show_snack_bar(page, f"Greška pri brisanju knjige: {message}", "ERROR")
            except Exception as e:
                show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
            finally:
                delete_dialog.open = False
                page.update()
        
        def cancel_delete(e):
            delete_dialog.open = False
            page.update()
        
        delete_dialog = ft.AlertDialog(
            title=ft.Text("Potvrda brisanja"),
            content=ft.Text("Da li ste sigurni da želite da obrišete ovu knjigu?"),
            actions=[
                ft.TextButton("Otkaži", on_click=cancel_delete),
                ft.TextButton("Obriši", on_click=confirm_delete, style=ft.ButtonStyle(color=ft.Colors.RED))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.dialog = delete_dialog
        delete_dialog.open = True
        page.update()
    
    # Create books table (desktop) and cards container (mobile)
    books_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Naslov")),
            ft.DataColumn(ft.Text("Autor")),
            ft.DataColumn(ft.Text("ISBN")),
            ft.DataColumn(ft.Text("Kategorija")),
            ft.DataColumn(ft.Text("Primerci")),
            ft.DataColumn(ft.Text("Lokacija")),
            ft.DataColumn(ft.Text("Akcije")),
        ],
        rows=[]
    )
    
    # Container for mobile cards
    books_container = ft.Column([], spacing=16)
    
    # Load books on page load
    load_books()
    
    # Navigation bar
    navbar_content = NavBar("admin", page_data)
    
    # Responsive content layout
    if is_mobile:
        content_layout = ft.Column([
            ft.Text("Upravljanje knjigama", size=24, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton(
                "Dodaj knjigu",
                icon=ft.Icons.ADD,
                on_click=lambda e: open_add_dialog(),
                expand=True,
                height=50
            ),
            ft.Divider(),
            search_query,
            ft.Divider(),
            books_container  # Mobile: cards
        ])
    else:
        content_layout = ft.Column([
            ft.Row([
                ft.Text("Upravljanje knjigama", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                ft.ElevatedButton(
                    "Dodaj knjigu",
                    icon=ft.Icons.ADD,
                    on_click=lambda e: open_add_dialog()
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            search_query,
            ft.Divider(),
            books_table  # Desktop: DataTable
        ])
    
    return ft.Column([
        navbar_content,
        ft.Container(
            content=ft.ListView(
                controls=[
                    ft.Card(
                        content=ft.Container(
                            content=content_layout,
                            padding=20 if not is_mobile else 10
                        )
                    ),
                    ft.Container(height=50)  # Bottom spacing
                ],
                spacing=10,
                padding=ft.padding.all(20 if not is_mobile else 10),
            ),
            expand=True,
            height=600,
        )
    ], expand=True)
