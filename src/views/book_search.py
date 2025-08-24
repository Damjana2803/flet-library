import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import SnackBar
from controllers.admin_controller import get_all_books, create_loan, create_reservation, has_member_borrowed_book, has_member_reserved_book
from utils.session_manager import get_current_user

def book_search(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Pretraga knjiga - Biblioteka"
    
    # Navigation bar
    navbar_content = NavBar("member", page_data)
    
    # Search results and filters
    search_results = []
    all_books = []
    
    # Book details fields (using Text components like in admin)
    detail_title = ft.Text("", size=20, weight=ft.FontWeight.BOLD)
    detail_author = ft.Text("", size=16)
    detail_isbn = ft.Text("", size=14)
    detail_category = ft.Text("", size=14)
    detail_year = ft.Text("", size=14)
    detail_publisher = ft.Text("", size=14)
    detail_location = ft.Text("", size=14)
    detail_copies = ft.Text("", size=14)
    detail_status = ft.Text("", size=14)
    detail_description = ft.Text("", size=14, color=ft.Colors.GREY_600)
    
    # Book details modal (using exact same pattern as admin books)
    details_modal_overlay = ft.Container(
        content=ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Text("Detalji knjige", size=20, weight=ft.FontWeight.BOLD, expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            on_click=lambda e: close_details_dialog(),
                            tooltip="Zatvori"
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_300)),
                    padding=ft.padding.only(bottom=20),
                ),
                ft.Container(
                    content=ft.Column([
                        detail_title,
                        detail_author,
                        detail_isbn,
                        detail_category,
                        detail_year,
                        detail_publisher,
                        detail_location,
                        detail_copies,
                        detail_status,
                        ft.Divider(height=16),
                        ft.Text("Opis:", size=14, weight=ft.FontWeight.BOLD),
                        detail_description,
                    ], spacing=8, scroll=ft.ScrollMode.AUTO),
                    padding=ft.padding.only(top=10),
                    expand=True,
                ),
            ], spacing=20),
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            width=500,
            margin=ft.margin.only(top=20, bottom=20),
        ),
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        visible=False,
    )
    
    def on_search(e):
        query = search_tf.value.strip() if search_tf.value else ""
        selected_category = category_dropdown.value
        selected_availability = availability_dropdown.value
        
        print(f"🔍 DEBUG: Search triggered")
        print(f"   Query: '{query}'")
        print(f"   Category: '{selected_category}'")
        print(f"   Availability: '{selected_availability}'")
        print(f"   Total books loaded: {len(all_books)}")
        
        # Filter books based on search query and filters
        filtered_books = []
        query_lower = query.lower()
        
        for book in all_books:
            # Check search query
            matches_query = not query or (
                query_lower in book.get("title", "").lower() or
                query_lower in book.get("author", "").lower() or
                query_lower in book.get("isbn", "").lower() or
                query_lower in book.get("category", "").lower()
            )
            
            # Check category filter - only apply if category is selected and not empty
            matches_category = True
            if selected_category and selected_category != "Sve kategorije":
                matches_category = book.get("category", "") == selected_category
            
            # Check availability filter - only apply if availability is selected and not empty
            matches_availability = True
            if selected_availability and selected_availability != "Sve":
                if selected_availability == "Dostupno":
                    matches_availability = book.get("available_copies", 0) > 0
                elif selected_availability == "Nedostupno":
                    matches_availability = book.get("available_copies", 0) == 0
            
            if matches_query and matches_category and matches_availability:
                filtered_books.append(book)
        
        print(f"   Books after filtering: {len(filtered_books)}")
        
        search_results.clear()
        search_results.extend(filtered_books)
        update_search_results()
    
    def on_category_change(e):
        print(f"📂 DEBUG: Category changed to: {category_dropdown.value}")
        on_search(None)
    
    def on_availability_change(e):
        print(f"📊 DEBUG: Availability changed to: {availability_dropdown.value}")
        on_search(None)
    
    def reset_filters(e):
        print(f"🔄 DEBUG: Resetting filters")
        search_tf.value = ""
        category_dropdown.value = "Sve kategorije"
        availability_dropdown.value = "Sve"
        print(f"   After reset - Search: '{search_tf.value}', Category: {category_dropdown.value}, Availability: {availability_dropdown.value}")
        on_search(None)
        page.update()
    
    def update_search_results():
        print(f"📋 DEBUG: Updating search results, count: {len(search_results)}")
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
                # Check if current user has borrowed or reserved this book
                current_user = get_current_user()
                member_id = current_user.get('member_id') if current_user else None
                
                is_borrowed = False
                is_reserved = False
                
                if member_id:
                    is_borrowed = has_member_borrowed_book(member_id, book.get('id'))
                    is_reserved = has_member_reserved_book(member_id, book.get('id'))
                
                # Create status indicators
                status_indicators = []
                
                # Availability status
                if book.get("available_copies", 0) > 0:
                    status_indicators.append(
                        ft.Container(
                            content=ft.Text("Dostupno", size=10, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.GREEN,
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=12,
                        )
                    )
                else:
                    status_indicators.append(
                        ft.Container(
                            content=ft.Text("Nedostupno", size=10, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.RED,
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=12,
                        )
                    )
                
                # Borrowed status
                if is_borrowed:
                    status_indicators.append(
                        ft.Container(
                            content=ft.Text("Iznajmljena", size=10, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.BLUE,
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=12,
                        )
                    )
                
                # Reserved status
                if is_reserved:
                    status_indicators.append(
                        ft.Container(
                            content=ft.Text("Rezervisana", size=10, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.ORANGE,
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=12,
                        )
                    )
                
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
                                                ft.Row(status_indicators, spacing=4),
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
                                            disabled=is_borrowed or is_reserved,  # Disable if already borrowed or reserved
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
            reserve_book(book)
    
    def borrow_book(book):
        """Borrow a book - create a new loan"""
        from datetime import datetime, timedelta
        
        # Get current user
        current_user = get_current_user()
        if not current_user:
            page.overlay.append(
                SnackBar("Morate biti prijavljeni da iznajmite knjigu!", duration=3000)
            )
            page.update()
            return
        
        # Get the member_id from the current user (not the user id)
        member_id = current_user.get('member_id')
        if not member_id:
            page.overlay.append(
                SnackBar("Član nije pronađen!", duration=3000)
            )
            page.update()
            return
        
        print(f"🔍 DEBUG: Borrowing book - Book ID: {book.get('id')}, Member ID: {member_id}")
        
        # Check if user can borrow more books
        current_loans = current_user.get('current_loans', 0)
        max_loans = current_user.get('max_loans', 5)
        
        if current_loans >= max_loans:
            page.overlay.append(
                SnackBar(f"Možete iznajmiti maksimalno {max_loans} knjiga!", duration=3000)
            )
            page.update()
            return
        
        # Use database function to create loan
        success, message = create_loan(
            book_id=book.get('id'),
            member_id=member_id  # Use member_id, not user id
        )
        
        print(f"🔍 DEBUG: Loan creation result - Success: {success}, Message: {message}")
        
        if success:
            # Show success message
            due_date = datetime.now() + timedelta(days=14)
            page.overlay.append(
                SnackBar(
                    f"Knjiga '{book['title']}' je uspešno iznajmljena! Vraćanje: {due_date.strftime('%d.%m.%Y')}",
                    duration=4000
                )
            )
            # Refresh search results to update availability
            load_books()
        else:
            page.overlay.append(
                SnackBar(f"Greška: {message}", duration=3000)
            )
        page.update()
    
    def reserve_book(book):
        """Reserve a book"""
        # Get current user
        current_user = get_current_user()
        if not current_user:
            page.overlay.append(
                SnackBar("Morate biti prijavljeni da rezervišete knjigu!", duration=3000)
            )
            page.update()
            return
        
        # Get the member_id from the current user (not the user id)
        member_id = current_user.get('member_id')
        if not member_id:
            page.overlay.append(
                SnackBar("Član nije pronađen!", duration=3000)
            )
            page.update()
            return
        
        print(f"🔍 DEBUG: Reserving book - Book ID: {book.get('id')}, Member ID: {member_id}")
        
        # Use database function to create reservation
        success, message = create_reservation(
            book_id=book.get('id'),
            member_id=member_id  # Use member_id, not user id
        )
        
        print(f"🔍 DEBUG: Reservation creation result - Success: {success}, Message: {message}")
        
        if success:
            page.overlay.append(
                SnackBar(f"Knjiga '{book['title']}' je uspešno rezervisana!", duration=4000)
            )
            # Refresh search results
            load_books()
        else:
            page.overlay.append(
                SnackBar(f"Greška: {message}", duration=3000)
            )
        page.update()
    
    def show_book_details(book):
        print(f"🔍 DEBUG: show_book_details called for book: {book.get('title')}")
        
        # Populate detail fields (exactly like admin does)
        detail_title.value = book["title"]
        detail_author.value = f"Autor: {book['author']}"
        detail_isbn.value = f"ISBN: {book['isbn']}"
        detail_category.value = f"Kategorija: {book['category']}"
        detail_year.value = f"Godina izdanja: {book['publication_year']}"
        detail_publisher.value = f"Izdavač: {book['publisher']}"
        detail_location.value = f"Lokacija: {book['location']}"
        detail_copies.value = f"Ukupno primeraka: {book['total_copies']}, Dostupno: {book['available_copies']}"
        detail_status.value = f"Status: {'Dostupno' if book.get('available_copies', 0) > 0 else 'Nedostupno'}"
        detail_status.color = ft.Colors.GREEN if book.get('available_copies', 0) > 0 else ft.Colors.RED
        detail_description.value = book.get('description', 'Nema opisa')
        
        # Show the modal (exactly like admin does)
        details_modal_overlay.visible = True
        page.update()
        print(f"✅ DEBUG: Modal opened for book: {book.get('title')}")
    
    def close_details_dialog():
        print(f"🔍 DEBUG: close_details_dialog called")
        details_modal_overlay.visible = False
        page.update()
        print(f"✅ DEBUG: Modal closed")
    
    def load_books():
        """Load all books from database and update category options"""
        nonlocal all_books
        all_books = get_all_books()
        print(f"📚 DEBUG: Loaded {len(all_books)} books from database")
        if all_books:
            print(f"   Sample book: {all_books[0]}")
        
        # Get unique categories from books
        categories = set()
        for book in all_books:
            if book.get("category"):
                categories.add(book.get("category"))
        
        # Update category dropdown options
        category_dropdown.options = [ft.dropdown.Option("Sve kategorije")] + [
            ft.dropdown.Option(cat) for cat in sorted(categories)
        ]
        category_dropdown.value = "Sve kategorije"
        
        print(f"   Available categories: {sorted(categories)}")
        
        on_search(None)
    
    # Search input
    search_tf = ft.TextField(
        label="Pretraži knjige...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        on_change=on_search,
    )
    
    # Filters
    category_dropdown = ft.Dropdown(
        label="Kategorija",
        options=[
            ft.dropdown.Option("Sve kategorije"),
        ],
        width=200,
        on_change=on_category_change,
        value="Sve kategorije",
    )
    
    availability_dropdown = ft.Dropdown(
        label="Dostupnost",
        options=[
            ft.dropdown.Option("Sve"),
            ft.dropdown.Option("Dostupno"),
            ft.dropdown.Option("Nedostupno"),
        ],
        width=200,
        on_change=on_availability_change,
        value="Sve",
    )
    
    # Reset button
    reset_button = ft.ElevatedButton(
        "Resetuj pretragu",
        icon=ft.Icons.REFRESH,
        on_click=reset_filters,
    )
    
    # Results column with ListView for better scrolling
    results_column = ft.Container(
        content=ft.ListView(
            controls=[],
            spacing=16,
            expand=True,
        ),
        expand=True,
        border=ft.border.all(1, ft.Colors.GREY_300),  # Add border to distinguish the scrollable area
        border_radius=8,
        padding=10,
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
                [search_tf],
                spacing=16,
            ),
            ft.Row(
                [category_dropdown, availability_dropdown, reset_button],
                spacing=16,
            ),
            results_column,
        ],
        spacing=20,
        expand=True,
    )
    
    # Load books on page load
    load_books()
    
    # Return using ft.Stack exactly like admin books (THE KEY!)
    return ft.Stack([
        ft.Column([
            navbar_content,
            ft.Container(
                content=content,
                padding=20,
                expand=True,
            ),
        ], expand=True),
        details_modal_overlay,  # Add the modal overlay on top
    ], expand=True)