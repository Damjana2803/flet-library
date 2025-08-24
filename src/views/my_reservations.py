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
    
    # Get real reservations data from database
    from controllers.admin_controller import get_member_reservations
    from utils.session_manager import get_current_user
    
    current_user = get_current_user()
    member_id = current_user.get('member_id')
    
    if member_id:
        reservations = get_member_reservations(member_id)
        # Add computed fields
        for reservation in reservations:
            # Convert string dates to datetime objects
            if isinstance(reservation['reservation_date'], str):
                reservation['reservation_date'] = datetime.fromisoformat(reservation['reservation_date'])
            if isinstance(reservation['expiry_date'], str):
                reservation['expiry_date'] = datetime.fromisoformat(reservation['expiry_date'])
            
            # Add computed fields
            reservation['priority'] = 1  # Default priority
            reservation['is_expired'] = reservation['expiry_date'] < datetime.now()
    else:
        reservations = []
    
    def load_reservations():
        """Load fresh reservations data from database and update UI"""
        nonlocal reservations
        from controllers.admin_controller import get_member_reservations
        from utils.session_manager import get_current_user
        
        current_user = get_current_user()
        member_id = current_user.get('member_id')
        
        if member_id:
            reservations = get_member_reservations(member_id)
            for reservation in reservations:
                if isinstance(reservation['reservation_date'], str):
                    reservation['reservation_date'] = datetime.fromisoformat(reservation['reservation_date'])
                if isinstance(reservation['expiry_date'], str):
                    reservation['expiry_date'] = datetime.fromisoformat(reservation['expiry_date'])
                reservation['priority'] = 1
                reservation['is_expired'] = reservation['expiry_date'] < datetime.now()
        else:
            reservations = []
        
        # Rebuild the entire page with fresh data
        page.clean()
        page.add(navbar_content)
        
        # Rebuild summary card with fresh data
        active_reservations = len([r for r in reservations if r["status"] == "active" and not r["is_expired"]])
        expired_reservations = len([r for r in reservations if r["is_expired"]])
        fulfilled_reservations = len([r for r in reservations if r["status"] == "fulfilled"])
        cancelled_reservations = len([r for r in reservations if r["status"] == "cancelled"])
        
        fresh_summary_card = ft.Card(
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
                                ft.Column(
                                    [
                                        ft.Text(
                                            str(cancelled_reservations),
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.GREY_600,
                                        ),
                                        ft.Text(
                                            "Otkazane",
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
        
        # Rebuild reservations list with fresh data
        fresh_reservations_list = ft.Column(
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
                                                    f"Autor: {reservation.get('book_author', 'Nepoznati autor')}",
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
                                                ) if reservation["status"] != "cancelled" else None,
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
                                            on_click=lambda e, r=reservation: cancel_reservation(r["id"]),
                                        ) if reservation["status"] == "active" and not reservation["is_expired"] else None,
                                        ft.TextButton(
                                            "Produži",
                                            icon=ft.Icons.REFRESH,
                                            on_click=lambda e, r=reservation: renew_reservation(r["id"]),
                                        ) if reservation["status"] == "active" and not reservation["is_expired"] else None,
                                    ] if button is not None],
                                    alignment=ft.MainAxisAlignment.END,
                                ) if reservation["status"] != "cancelled" else ft.Container(height=0),
                            ],
                            spacing=12,
                        ),
                        padding=16,
                    ),
                ) for reservation in reservations
            ],
            spacing=16,
        )
        
        page.add(ft.Container(
            content=ft.Column([
                fresh_summary_card,
                ft.Divider(height=32),
                fresh_reservations_list,
            ], scroll=ft.ScrollMode.AUTO),
            padding=20,
            expand=True,
        ))
        page.update()
    
    def cancel_reservation(reservation_id):
        """Cancel a reservation - mark it as cancelled in the database"""
        try:
            from controllers.admin_controller import cancel_reservation as db_cancel_reservation
            from utils.session_manager import get_current_user
            
            current_user = get_current_user()
            member_id = current_user.get('member_id')
            
            if member_id:
                success, message = db_cancel_reservation(reservation_id, member_id)
                
                if success:
                    page.overlay.append(
                        SnackBar("Rezervacija je uspešno otkazana!", duration=3000)
                    )
                    page.update()
                    # Refresh the data and update UI
                    load_reservations()
                else:
                    page.overlay.append(
                        SnackBar(f"Greška: {message}", snackbar_type="ERROR", duration=3000)
                    )
                    page.update()
            else:
                page.overlay.append(
                    SnackBar("Greška: Korisnik nije pronađen", snackbar_type="ERROR", duration=3000)
                )
                page.update()
                
        except Exception as e:
            page.overlay.append(
                SnackBar(f"Greška: {str(e)}", snackbar_type="ERROR", duration=3000)
            )
            page.update()
    
    def renew_reservation(reservation_id):
        """Renew a reservation - extend the expiry date by 7 days"""
        try:
            from controllers.admin_controller import renew_reservation as db_renew_reservation
            from utils.session_manager import get_current_user
            
            current_user = get_current_user()
            member_id = current_user.get('member_id')
            
            if member_id:
                success, message = db_renew_reservation(reservation_id, member_id)
                
                if success:
                    page.overlay.append(
                        SnackBar("Rezervacija je uspešno produžena za 7 dana!", duration=3000)
                    )
                    page.update()
                    # Refresh the data and update UI
                    load_reservations()
                else:
                    page.overlay.append(
                        SnackBar(f"Greška: {message}", snackbar_type="ERROR", duration=3000)
                    )
                    page.update()
            else:
                page.overlay.append(
                    SnackBar("Greška: Korisnik nije pronađen", snackbar_type="ERROR", duration=3000)
                )
                page.update()
                
        except Exception as e:
            page.overlay.append(
                SnackBar(f"Greška: {str(e)}", snackbar_type="ERROR", duration=3000)
            )
            page.update()
    
    def get_status_color(status, is_expired):
        if status == "fulfilled":
            return ft.Colors.GREEN
        elif status == "cancelled":
            return ft.Colors.GREY_600
        elif status == "expired" or is_expired:
            return ft.Colors.RED
        else:
            return ft.Colors.ORANGE
    
    def get_status_text(status, is_expired):
        if status == "fulfilled":
            return "Ispunjena"
        elif status == "cancelled":
            return "Otkazana"
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
                                                f"Autor: {reservation.get('book_author', 'Nepoznati autor')}",
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
                                            ) if reservation["status"] != "cancelled" else None,
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
                                        on_click=lambda e, r=reservation: cancel_reservation(r["id"]),
                                    ) if reservation["status"] == "active" and not reservation["is_expired"] else None,
                                    ft.TextButton(
                                        "Produži",
                                        icon=ft.Icons.REFRESH,
                                        on_click=lambda e, r=reservation: renew_reservation(r["id"]),
                                    ) if reservation["status"] == "active" and not reservation["is_expired"] else None,
                                ] if button is not None],
                                alignment=ft.MainAxisAlignment.END,
                            ) if reservation["status"] != "cancelled" else ft.Container(height=0),
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
    cancelled_reservations = len([r for r in reservations if r["status"] == "cancelled"])
    
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
                            ft.Column(
                                [
                                    ft.Text(
                                        str(cancelled_reservations),
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.GREY_600,
                                    ),
                                    ft.Text(
                                        "Otkazane",
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
        ft.Text(
            "Moje rezervacije",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900,
        ),
    ]
    
    # Add reservation cards directly to ListView
    if reservations:
        for reservation in reservations:
            reservation_card = ft.Card(
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
                                                f"Autor: {reservation.get('book_author', 'Nepoznati autor')}",
                                                size=14,
                                                color=ft.Colors.GREY_600,
                                            ),
                                            ft.Text(
                                                f"Rezervisano: {format_date(reservation['reservation_date'])}",
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
                                                f"Ističe: {format_date(reservation['expiry_date'])}",
                                                size=10,
                                                color=ft.Colors.GREY_500,
                                            ) if not reservation["is_expired"] else ft.Text(
                                                "Rezervacija je istekla",
                                                size=10,
                                                color=ft.Colors.RED,
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
                                        "Otkaži",
                                        icon=ft.Icons.CANCEL,
                                        on_click=lambda e, r=reservation: cancel_reservation(r["id"]),
                                    ) if reservation["status"] == "active" and not reservation["is_expired"] else None,
                                    ft.TextButton(
                                        "Produži",
                                        icon=ft.Icons.REFRESH,
                                        on_click=lambda e, r=reservation: renew_reservation(r["id"]),
                                    ) if reservation["status"] == "active" and not reservation["is_expired"] else None,
                                ] if button is not None],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ],
                        spacing=12,
                    ),
                    padding=16,
                ),
            )
            all_controls.append(reservation_card)
    else:
        all_controls.append(
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.BOOKMARK, size=48, color=ft.Colors.GREY_400),
                        ft.Text(
                            "Nemate aktivnih rezervacija",
                            size=16,
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=40,
                ),
            )
        )
    
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
