import flet as ft
import re

def main(page: ft.Page):
    page.title = "Booking Details"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def is_valid_finnish_phone(phone):
        phone = re.sub(r'[\s-]', '', phone)
        finnish_patterns = [
            r'^\+358[4-9]\d{7,8}$',
            r'^0[4-9]\d{7,8}$',
        ]
        return any(re.match(pattern, phone) for pattern in finnish_patterns)

    def validate_phone(e):
        if phone_field.value:
            if not is_valid_finnish_phone(phone_field.value):
                phone_field.error_text = "We currently provide services only in Finland. Please enter a valid Finnish phone number."
                phone_field.border_color = ft.colors.RED
            else:
                phone_field.error_text = None
                phone_field.border_color = ft.colors.GREY_400
        else:
            phone_field.error_text = None
            phone_field.border_color = ft.colors.GREY_400
        page.update()

    # Back button with icon
    back_button = ft.Row(
        [
            ft.Icon(ft.icons.ARROW_BACK, color=ft.colors.GREY_700, size=20),
            ft.Text("Back", color=ft.colors.GREY_700),
        ],
        spacing=5,
    )

    def validate_inputs(e):
        counter = 0
        if name_field.value:
            counter += 50
        
        if email_field.value:
            if is_valid_email(email_field.value):
                counter += 50
                email_field.error_text = None
                email_field.border_color = ft.colors.GREY_400
            else:
                email_field.error_text = "Please enter a valid email address"
                email_field.border_color = ft.colors.RED
        
        progress_bar.value = counter/100
        page.update()

    # Client Details Section (Left side)
    name_field = ft.TextField(
        label="Name",
        border_color=ft.colors.GREY_400,
        width=400,
        height=50,
        on_change=validate_inputs,
        hint_text="Enter your full name"
    )

    email_field = ft.TextField(
        label="Email",
        border_color=ft.colors.GREY_400,
        width=400,
        height=50,
        on_change=validate_inputs,
        hint_text="example@email.com"
    )

    progress_bar = ft.ProgressBar(
        width=400,
        value=0,
        color=ft.colors.BLUE_200,
        bgcolor=ft.colors.GREY_200,
    )

    phone_field = ft.TextField(
        label="Phone Number",
        border_color=ft.colors.GREY_400,
        width=400,
        height=50,
        hint_text="Finnish number (e.g., +358 40 1234567)",
        on_change=validate_phone
    )

    message_field = ft.TextField(
        label="Add Your Message",
        border_color=ft.colors.GREY_400,
        width=400,
        height=100,
        multiline=True,
        hint_text="Any special requests?"
    )

    # Booking Details Section (Right side)
    selected_service = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("Selected Service", size=16, color=ft.colors.GREY_700),
                    ft.Text("Trim", size=24, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.ACCESS_TIME, color=ft.colors.GREY_700, size=16),
                            ft.Text("1 hr", color=ft.colors.GREY_700, size=14),
                        ], spacing=5),
                        margin=ft.margin.only(top=5),
                    ),
                ]),
                bgcolor=ft.colors.BLUE_50,
                padding=15,
                border_radius=8,
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Date & Time", size=16, color=ft.colors.GREY_700),
                    ft.Row([
                        ft.Icon(ft.icons.CALENDAR_TODAY, color=ft.colors.GREY_700, size=16),
                        ft.Text("November 22, 2024", weight=ft.FontWeight.BOLD),
                    ], spacing=5),
                    ft.Row([
                        ft.Icon(ft.icons.ACCESS_TIME, color=ft.colors.GREY_700, size=16),
                        ft.Text("11:00 am", weight=ft.FontWeight.BOLD),
                    ], spacing=5),
                ]),
                padding=15,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=8,
                margin=ft.margin.only(top=10),
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Location", size=16, color=ft.colors.GREY_700),
                    ft.Row([
                        ft.Icon(ft.icons.LOCATION_ON, color=ft.colors.GREY_700, size=16),
                        ft.Text("San Francisco", weight=ft.FontWeight.BOLD),
                    ], spacing=5),
                ]),
                padding=15,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=8,
                margin=ft.margin.only(top=10),
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Staff", size=16, color=ft.colors.GREY_700),
                    ft.Row([
                        ft.Icon(ft.icons.PERSON, color=ft.colors.GREY_700, size=16),
                        ft.Text("Staff Member #1", weight=ft.FontWeight.BOLD),
                    ], spacing=5),
                ]),
                padding=15,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=8,
                margin=ft.margin.only(top=10),
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Price Details", size=16, color=ft.colors.GREY_700),
                    ft.Row([
                        ft.Text("Total", size=16),
                        ft.Text("$35", size=20, weight=ft.FontWeight.BOLD),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ]),
                padding=15,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=8,
                margin=ft.margin.only(top=10),
            ),
        ]),
        width=400,
    )

    def validate_form():
        if not name_field.value:
            name_field.error_text = "Name is required"
            page.update()
            return False
        
        if not email_field.value or not is_valid_email(email_field.value):
            email_field.error_text = "Please enter a valid email address"
            page.update()
            return False
            
        if phone_field.value and not is_valid_finnish_phone(phone_field.value):
            phone_field.error_text = "We currently provide services only in Finland. Please enter a valid Finnish phone number."
            page.update()
            return False
            
        return True

    def handle_add_to_cart(e):
        if validate_form():
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Added to cart!"), duration=3000)
            )

    def handle_book_now(e):
        if validate_form():
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Booking confirmed!"), duration=3000)
            )

    add_to_cart_btn = ft.ElevatedButton(
        text="Add to Cart",
        width=400,
        bgcolor=ft.colors.BLACK,
        color=ft.colors.WHITE,
        on_click=handle_add_to_cart,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )

    book_now_btn = ft.ElevatedButton(
        text="Book Now",
        width=400,
        bgcolor=ft.colors.BLACK,
        color=ft.colors.WHITE,
        on_click=handle_book_now,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )

    # Layout
    page.add(
        back_button,
        ft.Container(
            content=ft.Row([
                # Left column - Form
                ft.Column([
                    ft.Text("Client Details", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Tell us a bit about yourself"),
                    name_field,
                    email_field,
                    progress_bar,
                    phone_field,
                    message_field,
                ], spacing=20),
                
                # Right column - Selected service details
                ft.Column([
                    selected_service,
                    add_to_cart_btn,
                    book_now_btn,
                ], spacing=20),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=40),
            margin=ft.margin.only(top=20),
        )
    )

ft.app(target=main)
