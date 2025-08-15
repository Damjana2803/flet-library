import flet as ft
from flet_navigator import PageData
from components.navbar import NavBar
from components.snack_bar import SnackBar
from datetime import datetime, timedelta

def my_reservations(page_data: PageData) -> None:
    page = page_data.page
    page.title = "Moje rezervacije - Biblioteka"
    
    # Navigation bar
    navbar_content = NavBar("member", page_data)
    
    # Sample reservations data
    reservations = [
        {
            "id": 1,
            "book_title": "Ana Karenjina",
            "book_author": "Lav Tolstoj",
            "reservation_date": datetime.now() - timedelta(days=3),
            "expiry_date": datetime.now() + timedelta(days=4),
            "status": "active",
            "priority": 1,
            "is_expired": False
        },
        {
            "id": 2,
            "book_title": "Idiot",
            "book_author": "Fjodor Dostojevski",
            "reservation_date": datetime.now() - timedelta(days=8),
            "expiry_date": datetime.now() - timedelta(days=1),
            "status": "expired",
            "priority": 2,
            "is_expired": True
        },
        {
            "id": 3,
            "book_title": "Bratstvo Karamazovih",
            "book_author": "Fjodor Dostojevski",
            "reservation_date": datetime.now() - timedelta(days=10),
            "expiry_date": datetime.now() - timedelta(days=3),
            "status": "fulfilled",
            "priority": 1,
            "is_expired": False
        }
    ]
    
    def cancel_reservation(reservation_id):
        # In a real app, this would cancel the reservation
        page.overlay.append(
            SnackBar("Rezervacija je uspešno otkazana!", duration=3000)
        )
        page.update()
    
    def renew_reservation(reservation_id):
        # In a real app, this would extend the reservation
        page.overlay.append(
            SnackBar("Rezervacija je uspešno produžena za 7 dana!", duration=3000)
        )
        page.update()
    
    def get_status_color(status, is_expired):
        if status == "fulfilled":
            return ft.Colors.GREEN
        elif status == "expired" or is_expired:
            return ft.Colors.RED
        else:
            return ft.Colors.ORANGE
    
    def get_status_text(status, is_expired):
        if status == "fulfilled":
            return "Ispunjena"
        elif status == "expired" or is_expired:
            return "Istekla"
        else:
            return "Aktivna"
    
    def format_date(date):
        return date.strftime("%d.%m.%Y")
    
    def get_days_until_expiry(expiry_date):
        remaining = (expiry_date - datetime.now()).days
        return max(0, remaining)
    
    # Reservations list
    reservations_list = ft.Column(
        [
            ft.Text(
                "Moje rezervacije",
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
                                        ft.Icons.BOOKMARK,
                                        color=get_status_color(reservation["status"], reservation["is_expired"]),
                                        size=24,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(
                                                reservation["book_title"],
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(
                                                f"Autor: {reservation['book_author']}",
                                                size=14,
                                                color=ft.Colors.GREY_600,
                                            ),
                                            ft.Text(
                                                f"Rezervisano: {format_date(reservation['reservation_date'])}",
                                                size=12,
                                                color=ft.Colors.GREY_500,
                                            ),
                                            ft.Text(
                                                f"Prioritet: {reservation['priority']}",
                                                size=12,
                                                color=ft.Colors.GREY_500,
                                            ),
                                        ],
                                        expand=True,
                                    ),
                                    ft.Column(
                                        [item for item in [
                                            ft.Text(
                                                get_status_text(reservation["status"], reservation["is_expired"]),
                                                size=12,
                                                color=get_status_color(reservation["status"], reservation["is_expired"]),
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(
                                                f"Istek: {format_date(reservation['expiry_date'])}" if not reservation["is_expired"] and reservation["status"] == "active" else f"Isteklo: {format_date(reservation['expiry_date'])}",
                                                size=10,
                                                color=ft.Colors.GREY_500 if not reservation["is_expired"] and reservation["status"] == "active" else ft.Colors.RED,
                                            ),
                                            ft.Text(
                                                f"Preostalo: {get_days_until_expiry(reservation['expiry_date'])} dana",
                                                size=10,
                                                color=ft.Colors.ORANGE if get_days_until_expiry(reservation['expiry_date']) <= 2 else ft.Colors.GREY_500,
                                                weight=ft.FontWeight.BOLD if get_days_until_expiry(reservation['expiry_date']) <= 2 else ft.FontWeight.NORMAL,
                                            ) if reservation["status"] == "active" and not reservation["is_expired"] else None,
                                        ] if item is not None],
                                        horizontal_alignment=ft.CrossAxisAlignment.END,
                                    ),
                                ],
                                spacing=16,
                            ),
                            ft.Row(
                                [button for button in [
                                    ft.TextButton(
                                        "Otkaži",
                                        icon=ft.Icons.CANCEL,
                                        on_click=lambda r=reservation: cancel_reservation(r["id"]),
                                    ) if reservation["status"] == "active" and not reservation["is_expired"] else None,
                                    ft.TextButton(
                                        "Produži",
                                        icon=ft.Icons.REFRESH,
                                        on_click=lambda r=reservation: renew_reservation(r["id"]),
                                    ) if reservation["status"] == "active" and not reservation["is_expired"] else None,
                                ] if button is not None],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ],
                        spacing=12,
                    ),
                    padding=16,
                ),
            ) for reservation in reservations
        ],
        spacing=16,
    )
    
    # Summary card
    active_reservations = len([r for r in reservations if r["status"] == "active" and not r["is_expired"]])
    expired_reservations = len([r for r in reservations if r["is_expired"]])
    fulfilled_reservations = len([r for r in reservations if r["status"] == "fulfilled"])
    
    summary_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Pregled rezervacija",
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
                                        str(active_reservations),
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.ORANGE,
                                    ),
                                    ft.Text(
                                        "Aktivne",
                                        size=12,
                                        color=ft.Colors.GREY_600,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                expand=True,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        str(expired_reservations),
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.RED,
                                    ),
                                    ft.Text(
                                        "Istekle",
                                        size=12,
                                        color=ft.Colors.GREY_600,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                expand=True,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        str(fulfilled_reservations),
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.GREEN,
                                    ),
                                    ft.Text(
                                        "Ispunjene",
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
            reservations_list,
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
