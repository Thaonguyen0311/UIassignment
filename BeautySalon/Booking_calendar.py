import flet as ft
from datetime import datetime, timedelta
import calendar

def main(page: ft.Page):
    page.title = "Booking Application"
    page.padding = 10
    page.window_width = 1000
    page.window_height = 800
    page.window_resizable = False
    
    # Track current display date separately from today's date
    current_display_date = datetime.now()
    
    selected_date_text = ft.Text(
        "Saturday, November 9",
        size=14,
        weight=ft.FontWeight.W_500
    )
    
    # Add state for selected time
    selected_time = ft.Text(
        "Select a time",
        size=14,
        weight=ft.FontWeight.W_500
    )
    
    def date_clicked(e, day):
        clicked_date = datetime(current_display_date.year, current_display_date.month, day)
        selected_date_text.value = clicked_date.strftime("%A, %B %d")
        # Reset selected time when date changes
        selected_time.value = "Select a time"
        # Reset all time slot colors
        for slot in time_slots_grid.controls:
            for container in slot.controls:
                container.bgcolor = "white"
                container.content.color = "black"
        page.update()

    def time_slot_clicked(e, time_container):
        # Reset all time slot colors
        for slot in time_slots_grid.controls:
            for container in slot.controls:
                container.bgcolor = "white"
                container.content.color = "black"
        
        # Highlight selected time slot
        time_container.bgcolor = "black"
        time_container.content.color = "white"
        
        # Update selected time text
        selected_time.value = f"Time: {time_container.content.value}"
        page.update()

    time_slots_grid = ft.Column(spacing=5)
    def create_time_slots():
        times = [
            "11:30 am", "12:00 pm", "12:30 pm", "1:00 pm",
            "1:30 pm", "2:00 pm", "2:30 pm", "3:00 pm",
            "3:30 pm", "4:00 pm"
        ]
        
        for i in range(0, len(times), 2):
            row = ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(times[i], size=14),
                        width=120,
                        height=35,
                        border=ft.border.all(1, "black"),
                        border_radius=5,
                        padding=5,
                        alignment=ft.alignment.center,
                        bgcolor="white",
                        on_click=lambda e, t=times[i]: time_slot_clicked(e, e.control)
                    )
                ],
                spacing=10
            )
            if i + 1 < len(times):
                row.controls.append(
                    ft.Container(
                        content=ft.Text(times[i + 1], size=14),
                        width=120,
                        height=35,
                        border=ft.border.all(1, "black"),
                        border_radius=5,
                        padding=5,
                        alignment=ft.alignment.center,
                        bgcolor="white",
                        on_click=lambda e, t=times[i + 1]: time_slot_clicked(e, e.control)
                    )
                )
            time_slots_grid.controls.append(row)
        return time_slots_grid

    # Reference to month text for updating
    month_text = ft.Text(
        datetime.now().strftime("%B %Y"),
        size=16,
        weight=ft.FontWeight.W_500
    )

    # Reference to calendar grid for updating
    calendar_column = ft.Column(spacing=5)

    def update_calendar():
        # Clear existing calendar rows (keep header row)
        while len(calendar_column.controls) > 2:
            calendar_column.controls.pop()

        # Get calendar for current month
        cal = calendar.monthcalendar(current_display_date.year, current_display_date.month)
        
        # Update month text
        month_text.value = current_display_date.strftime("%B %Y")
        
        # Add new calendar rows
        for week in cal:
            week_row = ft.Row(spacing=0)
            for day in week:
                if day == 0:
                    day_button = ft.Container(width=40, height=30)
                else:
                    day_button = ft.ElevatedButton(
                        text=str(day),
                        width=40,
                        height=30,
                        style=ft.ButtonStyle(
                            padding=2,
                            shape=ft.RoundedRectangleBorder(radius=5),
                        ),
                        on_click=lambda e, d=day: date_clicked(e, d)
                    )
                week_row.controls.append(day_button)
            calendar_column.controls.append(week_row)
        
        page.update()

    def previous_month(e):
        nonlocal current_display_date
        # Move to previous month
        if current_display_date.month == 1:
            current_display_date = current_display_date.replace(year=current_display_date.year - 1, month=12)
        else:
            current_display_date = current_display_date.replace(month=current_display_date.month - 1)
        update_calendar()

    def next_month(e):
        nonlocal current_display_date
        # Move to next month
        if current_display_date.month == 12:
            current_display_date = current_display_date.replace(year=current_display_date.year + 1, month=1)
        else:
            current_display_date = current_display_date.replace(month=current_display_date.month + 1)
        update_calendar()

    def create_calendar():
        # Add header row with month and navigation
        calendar_column.controls = [
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.CHEVRON_LEFT,
                        icon_size=20,
                        on_click=previous_month
                    ),
                    month_text,
                    ft.IconButton(
                        icon=ft.icons.CHEVRON_RIGHT,
                        icon_size=20,
                        on_click=next_month
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Row(
                controls=[
                    ft.Text(
                        day, 
                        width=40, 
                        text_align=ft.TextAlign.CENTER,
                        size=14
                    )
                    for day in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
                ],
            ),
        ]
        
        # Add initial calendar
        update_calendar()
        
        return calendar_column

    def check_availability():
        if selected_time.value != "Select a time":
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Booking confirmed for {selected_date_text.value} at {selected_time.value.replace('Time: ', '')}")
                )
            )
        else:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Please select a time slot")
                )
            )

    # Create main layout
    main_content = ft.Row(
        controls=[
            # Left side - Calendar and Time slots
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Select a Date and Time",
                            size=20,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(
                                    "Timezone: Pacific Standard Time (PST)",
                                    size=14
                                ),
                                ft.Icon(
                                    ft.icons.ARROW_DROP_DOWN,
                                    size=20
                                ),
                            ],
                        ),
                        create_calendar(),
                        ft.Divider(height=1),
                        selected_date_text,
                        create_time_slots(),
                    ],
                    spacing=10,
                ),
                padding=10,
                expand=True,
            ),
            ft.VerticalDivider(width=1),
            # Right side - Booking Details
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Booking Details",
                            size=20,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Wash & Dry", size=16),
                                ft.Text("1 hr", size=14),
                                ft.Text("San Francisco", size=14),
                                selected_time,
                            ],
                            spacing=5,
                        ),
                        ft.ElevatedButton(
                            "Next",
                            bgcolor="black",
                            color="white",
                            width=200,
                            height=35,
                            on_click=lambda e: check_availability()
                        ),
                    ],
                    spacing=10,
                ),
                padding=10,
                width=250,
            ),
        ],
        spacing=0,
        height=600,
    )

    page.add(main_content)
    page.update()

ft.app(target=main)
