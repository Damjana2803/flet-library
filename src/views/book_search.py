import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import SnackBar
from controllers.admin_controller import get_all_books, create_loan, create_reservation
from utils.session_manager import get_current_user

def book_search(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Pretraga knjiga - Biblioteka"
    
    # Navigation bar
    navbar_content = NavBar("member", page_data)
    
    # Search results and filters
    search_results = []
    all_books = []
    
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
            member_id=current_user.get('id')
        )
        
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
        
        # Use database function to create reservation
        success, message = create_reservation(
            book_id=book.get('id'),
            member_id=current_user.get('id')
        )
        
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
        # Show book details modal
        page.dialog = ft.AlertDialog(
            title=ft.Text(book["title"]),
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"Autor: {book['author']}", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"ISBN: {book['isbn']}", size=14),
                            ft.Text(f"Kategorija: {book['category']}", size=14),
                            ft.Text(f"Godina izdanja: {book['publication_year']}", size=14),
                            ft.Text(f"Izdavač: {book['publisher']}", size=14),
                            ft.Text(f"Lokacija: {book['location']}", size=14),
                            ft.Text(f"Ukupno primeraka: {book['total_copies']}", size=14),
                            ft.Text(f"Dostupno primeraka: {book['available_copies']}", size=14),
                            ft.Text(
                                f"Status: {'Dostupno' if book.get('available_copies', 0) > 0 else 'Nedostupno'}",
                                size=14,
                                color=ft.Colors.GREEN if book.get('available_copies', 0) > 0 else ft.Colors.RED,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Divider(height=16),
                            ft.Text("Opis:", size=14, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                book.get('description', 'Nema opisa'),
                                size=14,
                                color=ft.Colors.GREY_600,
                            ),
                        ], spacing=8),
                        padding=20,
                    )
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
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    
    # Load all books when page opens
    load_books()
    
    return ft.Column([
        navbar_content,
        ft.Container(
            content=ft.Column(
                [content],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=20,
            expand=True,
        )
    ], expand=True)
