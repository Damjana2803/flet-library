import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import SnackBar
from utils.global_state import global_state
from datetime import datetime, timedelta

def admin_statistics(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Statistike - Biblioteka"
    
    # Navigation bar
    navbar_content = NavBar("admin", page_data)
    
    # Get real data from global state
    books = global_state.get("books", [])
    members = global_state.get("members", [])
    loans = global_state.get("loans", [])
    
    # Calculate real statistics
    total_books = len(books)
    total_members = len(members)
    active_loans = len([loan for loan in loans if loan.get('status') == 'active'])
    
    # Calculate available books
    available_books = len([book for book in books if book.get('available_copies', 0) > 0])
    
    # Calculate member types
    student_members = len([m for m in members if m.get('membership_type') == 'student'])
    regular_members = len([m for m in members if m.get('membership_type') == 'regular'])
    senior_members = len([m for m in members if m.get('membership_type') == 'senior'])
    
    # Calculate active members
    active_members = len([m for m in members if m.get('membership_status') == 'active'])
    
    # Real statistics data
    stats_data = {
        "total_books": total_books,
        "available_books": available_books,
        "total_members": total_members,
        "active_members": active_members,
        "active_loans": active_loans
    }
    
    # Calculate popular books from real loan data
    book_loan_counts = {}
    for loan in loans:
        book_title = loan.get('book_title', 'Nepoznata knjiga')
        book_author = loan.get('book_author', 'Nepoznati autor')
        book_key = f"{book_title}|{book_author}"
        
        if book_key not in book_loan_counts:
            book_loan_counts[book_key] = {
                "title": book_title,
                "author": book_author,
                "loans": 0
            }
        book_loan_counts[book_key]["loans"] += 1
    
    # Sort by loan count and get top 5
    popular_books = sorted(book_loan_counts.values(), key=lambda x: x["loans"], reverse=True)[:5]
    
    # If no loan data, show sample data
    if not popular_books:
        popular_books = [
            {"title": "Nema podataka", "author": "Nema podataka", "loans": 0}
        ]
    
    # Calculate real membership data
    total_members_for_percentage = total_members if total_members > 0 else 1
    
    membership_data = [
        {"type": "Redovno članstvo", "count": regular_members, "percentage": round((regular_members / total_members_for_percentage) * 100, 1)},
        {"type": "Studentsko članstvo", "count": student_members, "percentage": round((student_members / total_members_for_percentage) * 100, 1)},
        {"type": "Penzionersko članstvo", "count": senior_members, "percentage": round((senior_members / total_members_for_percentage) * 100, 1)}
    ]
    

    
    def export_report(e):
        # In a real app, this would generate and download a report
        page.overlay.append(
            SnackBar("Izveštaj je uspešno preuzet!", duration=3000)
        )
        page.update()
    
    # Statistics cards
    def create_stat_card(title, value, icon, color):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(icon, size=32, color=color),
                        ft.Text(
                            str(value),
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=color,
                        ),
                        ft.Text(
                            title,
                            size=14,
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
    
    # Main statistics row
    stats_row = ft.Row(
        [
            create_stat_card("Ukupno knjiga", stats_data["total_books"], ft.Icons.BOOK, ft.Colors.BLUE),
            create_stat_card("Dostupno knjiga", stats_data["available_books"], ft.Icons.CHECK_CIRCLE, ft.Colors.GREEN),
            create_stat_card("Aktivnih članova", stats_data["active_members"], ft.Icons.PEOPLE, ft.Colors.ORANGE),
            create_stat_card("Iznajmljeno", stats_data["active_loans"], ft.Icons.LIBRARY_BOOKS, ft.Colors.PURPLE),
        ],
        spacing=16,
    )
    
    # Additional statistics row
    additional_stats_row = ft.Row(
        [
            create_stat_card("Ukupno članova", stats_data["total_members"], ft.Icons.GROUP, ft.Colors.TEAL),
        ],
        spacing=16,
    )
    
    # Popular books list
    popular_books_list = ft.Column(
        [
            ft.Text(
                "Najtraženije knjige",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_900,
            ),
        ] + [
            ft.ListTile(
                leading=ft.Icon(ft.Icons.BOOK, color=ft.Colors.BLUE),
                title=ft.Text(book["title"]),
                subtitle=ft.Text(f"Autor: {book['author']}"),
                trailing=ft.Text(
                    f"{book['loans']} iznajmljivanja",
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE,
                ),
            ) for book in popular_books
        ],
        spacing=8,
    )
    
    # Membership distribution
    membership_chart = ft.Column(
        [
            ft.Text(
                "Distribucija članstva",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_900,
            ),
        ] + [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(member["type"], expand=True),
                                ft.Text(f"{member['count']} ({member['percentage']}%)"),
                            ],
                        ),
                        ft.ProgressBar(
                            value=member["percentage"] / 100,
                            color=ft.Colors.BLUE,
                            bgcolor=ft.Colors.GREY_300,
                        ),
                    ],
                    spacing=4,
                ),
                padding=ft.padding.only(bottom=16),
            ) for member in membership_data
        ],
        spacing=8,
    )
    

    
    # Main content
    content = ft.Column(
        [
            ft.Row(
                [
                    ft.Text(
                        "Statistike biblioteke",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),
                    ft.ElevatedButton(
                        "Izvezi izveštaj",
                        icon=ft.Icons.DOWNLOAD,
                        on_click=export_report,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(height=32),
            stats_row,
            ft.Divider(height=16),
            additional_stats_row,
            ft.Divider(height=32),
            ft.Row(
                [
                    ft.Column([popular_books_list], expand=True),
                    ft.VerticalDivider(width=32),
                    ft.Column([membership_chart], expand=True),
                ],
                spacing=32,
            ),

        ],
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    
    return ft.Column([
        navbar_content,
        ft.Container(
            content=content,
            padding=20,
            expand=True,
            height=600,

        )
    ], expand=True)
