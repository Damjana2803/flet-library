import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import show_snack_bar
from controllers.admin_controller import add_book, get_all_books, delete_book, update_book

def admin_books(page_data: PageData):
    page = page_data.page
    page.title = "Upravljanje knjigama - Biblioteka"
    
    # Check if mobile screen
    is_mobile = page.width < 768 if page.width else False
    
    # State variables
    books = []
    show_modal = False  # Control modal visibility
    search_query = ft.TextField(
        label="Pretraži knjige",
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: filter_books()
    )
    
    # Dialog fields for adding new book
    title_field = ft.TextField(
        hint_text="Orlovi rano lete",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(title_field, "Naslov je obavezan")
    )
    author_field = ft.TextField(
        hint_text="Branko Ćopić",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(author_field, "Autor je obavezan")
    )
    isbn_field = ft.TextField(
        hint_text="978-86-123-4567-8",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(isbn_field, "ISBN je obavezan")
    )
    category_field = ft.TextField(
        hint_text="Literatura",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400)
    )
    year_field = ft.TextField(
        hint_text="2020",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(year_field, "Godina je obavezna")
    )
    publisher_field = ft.TextField(
        hint_text="Vulkan izdavaštvo",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400)
    )
    description_field = ft.TextField(
        multiline=True, 
        min_lines=3, 
        max_lines=5, 
        hint_text="Kratak opis knjige, radnja, žanr...",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400)
    )
    copies_field = ft.TextField(
        hint_text="5",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(copies_field, "Broj primeraka je obavezan")
    )
    location_field = ft.TextField(
        hint_text="Polica A-28",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400)
    )
    
    # Edit book dialog fields
    edit_title_field = ft.TextField(
        hint_text="Orlovi rano lete",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(edit_title_field, "Naslov je obavezan")
    )
    edit_author_field = ft.TextField(
        hint_text="Branko Ćopić",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(edit_author_field, "Autor je obavezan")
    )
    edit_isbn_field = ft.TextField(
        hint_text="978-86-123-4567-8",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(edit_isbn_field, "ISBN je obavezan")
    )
    edit_category_field = ft.TextField(
        hint_text="Literatura",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400)
    )
    edit_year_field = ft.TextField(
        hint_text="2020",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(edit_year_field, "Godina je obavezna")
    )
    edit_publisher_field = ft.TextField(
        hint_text="Vulkan izdavaštvo",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400)
    )
    edit_description_field = ft.TextField(
        multiline=True, 
        min_lines=3, 
        max_lines=5, 
        hint_text="Kratak opis knjige, radnja, žanr...",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400)
    )
    edit_copies_field = ft.TextField(
        hint_text="5",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        on_change=lambda e: validate_field(edit_copies_field, "Broj primeraka je obavezan")
    )
    edit_location_field = ft.TextField(
        hint_text="Polica A-28",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400)
    )
    
    # Custom modal overlays
    # Add book modal
    add_modal_overlay = ft.Container(
        content=ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Text("Dodaj novu knjigu", size=20, weight=ft.FontWeight.BOLD, expand=True),
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
                        ft.Text("Naslov *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        title_field,
                        ft.Text("Autor *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        author_field,
                        ft.Text("ISBN *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        isbn_field,
                        ft.Text("Kategorija", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        category_field,
                        ft.Text("Godina izdanja *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        year_field,
                        ft.Text("Izdavač", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        publisher_field,
                        ft.Text("Opis", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        description_field,
                        ft.Text("Broj primeraka *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        copies_field,
                        ft.Text("Lokacija", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        location_field
                    ], spacing=5, scroll=ft.ScrollMode.AUTO),
                    padding=ft.padding.only(top=10),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton("Otkaži", on_click=lambda e: close_add_dialog()),
                        ft.ElevatedButton("Dodaj", on_click=lambda e: save_book(), style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)),
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
    
    # Edit book modal
    edit_modal_overlay = ft.Container(
        content=ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Text("Izmeni knjigu", size=20, weight=ft.FontWeight.BOLD, expand=True),
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
                        ft.Text("Naslov *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_title_field,
                        ft.Text("Autor *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_author_field,
                        ft.Text("ISBN *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_isbn_field,
                        ft.Text("Kategorija", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_category_field,
                        ft.Text("Godina izdanja *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_year_field,
                        ft.Text("Izdavač", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_publisher_field,
                        ft.Text("Opis", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_description_field,
                        ft.Text("Broj primeraka *", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_copies_field,
                        ft.Text("Lokacija", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        edit_location_field
                    ], spacing=5, scroll=ft.ScrollMode.AUTO),
                    padding=ft.padding.only(top=10),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton("Otkaži", on_click=lambda e: close_edit_dialog()),
                        ft.ElevatedButton("Sačuvaj", on_click=lambda e: update_book_action(), style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)),
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
                ft.Text("Da li ste sigurni da želite da obrišete ovu knjigu?", size=16),
                ft.Row([
                    ft.ElevatedButton("Otkaži", on_click=lambda e: close_delete_dialog()),
                    ft.ElevatedButton("Obriši", on_click=lambda e: confirm_delete_book(), style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)),
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
    
    # Variable to store book being deleted
    current_deleting_book_id = None
    
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
        
        # Validate add fields
        if not title_field.value or title_field.value.strip() == "":
            title_field.border_color = ft.Colors.RED
            title_field.error_text = "Naslov je obavezan"
            is_valid = False
        
        if not author_field.value or author_field.value.strip() == "":
            author_field.border_color = ft.Colors.RED
            author_field.error_text = "Autor je obavezan"
            is_valid = False
        
        if not isbn_field.value or isbn_field.value.strip() == "":
            isbn_field.border_color = ft.Colors.RED
            isbn_field.error_text = "ISBN je obavezan"
            is_valid = False
        
        if not year_field.value or year_field.value.strip() == "":
            year_field.border_color = ft.Colors.RED
            year_field.error_text = "Godina je obavezna"
            is_valid = False
        
        if not copies_field.value or copies_field.value.strip() == "":
            copies_field.border_color = ft.Colors.RED
            copies_field.error_text = "Broj primeraka je obavezan"
            is_valid = False
        
        page.update()
        return is_valid
    
    def validate_all_edit_fields():
        """Validate all required edit fields and return True if all valid"""
        is_valid = True
        
        # Validate edit fields
        if not edit_title_field.value or edit_title_field.value.strip() == "":
            edit_title_field.border_color = ft.Colors.RED
            edit_title_field.error_text = "Naslov je obavezan"
            is_valid = False
        
        if not edit_author_field.value or edit_author_field.value.strip() == "":
            edit_author_field.border_color = ft.Colors.RED
            edit_author_field.error_text = "Autor je obavezan"
            is_valid = False
        
        if not edit_isbn_field.value or edit_isbn_field.value.strip() == "":
            edit_isbn_field.border_color = ft.Colors.RED
            edit_isbn_field.error_text = "ISBN je obavezan"
            is_valid = False
        
        if not edit_year_field.value or edit_year_field.value.strip() == "":
            edit_year_field.border_color = ft.Colors.RED
            edit_year_field.error_text = "Godina je obavezna"
            is_valid = False
        
        if not edit_copies_field.value or edit_copies_field.value.strip() == "":
            edit_copies_field.border_color = ft.Colors.RED
            edit_copies_field.error_text = "Broj primeraka je obavezan"
            is_valid = False
        
        page.update()
        return is_valid
    
    def open_add_dialog():
        try:
            # Show the custom modal
            nonlocal show_modal
            show_modal = True
            add_modal_overlay.visible = True
            page.update()
            
        except Exception as e:
            show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
    
    def close_add_dialog():
        nonlocal show_modal
        show_modal = False
        add_modal_overlay.visible = False
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
        
        # Show the edit modal
        edit_modal_overlay.visible = True
        page.update()
    
    def close_edit_dialog():
        edit_modal_overlay.visible = False
        page.update()
    
    def save_book():
        try:
            # Validate all required fields first
            if not validate_all_fields():
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
            # Validate all required fields first
            if not validate_all_edit_fields():
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
        
        # Clear validation errors
        title_field.border_color = None
        title_field.error_text = None
        author_field.border_color = None
        author_field.error_text = None
        isbn_field.border_color = None
        isbn_field.error_text = None
        year_field.border_color = None
        year_field.error_text = None
        copies_field.border_color = None
        copies_field.error_text = None
        
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
        
        # Clear validation errors
        edit_title_field.border_color = None
        edit_title_field.error_text = None
        edit_author_field.border_color = None
        edit_author_field.error_text = None
        edit_isbn_field.border_color = None
        edit_isbn_field.error_text = None
        edit_year_field.border_color = None
        edit_year_field.error_text = None
        edit_copies_field.border_color = None
        edit_copies_field.error_text = None
        
        page.update()
    
    def load_books():
        try:
            all_books = get_all_books()
            books.clear()
            books.extend(all_books)
            
            # If no books exist in database, add some sample books using the database function
            if not books:
                sample_books = [
                    {
                        'title': 'Prvi korak u programiranju',
                        'author': 'Marko Petrović',
                        'isbn': '978-86-123-4567-8',
                        'category': 'Programiranje',
                        'publication_year': 2023,
                        'publisher': 'Tehnička knjiga',
                        'description': 'Uvod u programiranje za početnike',
                        'total_copies': 5,
                        'location': 'Glavna biblioteka'
                    },
                    {
                        'title': 'Baze podataka',
                        'author': 'Ana Jovanović',
                        'isbn': '978-86-234-5678-9',
                        'category': 'Baze podataka',
                        'publication_year': 2022,
                        'publisher': 'Fakultet organizacionih nauka',
                        'description': 'Teorija i praksa baza podataka',
                        'total_copies': 3,
                        'location': 'Glavna biblioteka'
                    }
                ]
                
                # Add sample books to database
                for book_data in sample_books:
                    success, message = add_book(**book_data)
                    if not success:
                        print(f"Greška pri dodavanju sample knjige: {message}")
                
                # Reload books from database after adding sample data
                all_books = get_all_books()
                books.clear()
                books.extend(all_books)
            
            update_books_table()
        except Exception as e:
            print(f"Greška pri učitavanju knjiga: {str(e)}")
            show_snack_bar(page, f"Greška pri učitavanju knjiga: {str(e)}", "ERROR")
    
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
        nonlocal current_deleting_book_id
        current_deleting_book_id = book_id
        
        # Show the delete confirmation modal
        delete_modal_overlay.visible = True
        page.update()
    
    def close_delete_dialog():
        delete_modal_overlay.visible = False
        page.update()
    
    def confirm_delete_book():
        try:
            success, message = delete_book(current_deleting_book_id)
            if success:
                show_snack_bar(page, "Knjiga uspešno obrisana!", "SUCCESS")
                load_books()
            else:
                show_snack_bar(page, f"Greška pri brisanju knjige: {message}", "ERROR")
        except Exception as e:
            show_snack_bar(page, f"Greška: {str(e)}", "ERROR")
        finally:
            close_delete_dialog()
    
    # Create books table (desktop) and cards container (mobile)
    books_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Naslov"), numeric=False),
            ft.DataColumn(ft.Text("Autor"), numeric=False),
            ft.DataColumn(ft.Text("ISBN"), numeric=False),
            ft.DataColumn(ft.Text("Kategorija"), numeric=False),
            ft.DataColumn(ft.Text("Primerci"), numeric=False),
            ft.DataColumn(ft.Text("Lokacija"), numeric=False),
            ft.DataColumn(ft.Text("Akcije"), numeric=False),
        ],
        rows=[],
        expand=True,  # Make table take full width
        width=float('inf')  # Force full width
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
        ], scroll=ft.ScrollMode.AUTO, expand=True)
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
            ft.Container(
                content=books_table,
                expand=True,
                width=float('inf')
            )  # Desktop: DataTable
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    return ft.Stack([
        ft.Column([
            navbar_content,
            ft.Container(
                content=content_layout,
                padding=20 if not is_mobile else 10,
                expand=True
            )
        ], expand=True),
        add_modal_overlay,  # Add the modal overlay on top
        edit_modal_overlay,
        delete_modal_overlay
    ], expand=True)