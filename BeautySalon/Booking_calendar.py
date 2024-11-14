import flet as ft
from datetime import datetime, timedelta
import calendar

def main(page: ft.Page):
    # Initial setup
    page.route_data = {
        "service": "Wash & Dry",
        "duration": "1 hr",
        "location": "San Francisco"
    }
    
    page.title = "Booking Application"
    page.padding = 20
    page.window_width = 1200
    page.window_height = 700
    page.window_resizable = False
    
    current_display_date = datetime.now()
    today = datetime.now().date()
    selected_date = None
    
    booking_details = {
        "service": page.route_data.get("service", ""),
        "duration": page.route_data.get("duration", ""),
        "location": page.route_data.get("location", ""),
        "date": "",
        "time": ""
    }
    
    selected_date_text = ft.Text(
        "Select a date",
        size=14,
        weight=ft.FontWeight.W_500
    )

    month_text = ft.Text(
        datetime.now().strftime("%B %Y"),
        size=24,
        weight=ft.FontWeight.W_300,
        color="#000000"
    )

    calendar_column = ft.Column(spacing=5)

    # Function definitions
    def close_dialog(e):
        dialog.open = False
        page.update()

    def navigate_to_next_page(e):
        dialog_content = ft.Column(
            controls=[
                ft.Text(f"Service: {booking_details['service']}"),
                ft.Text(f"Duration: {booking_details['duration']}"),
                ft.Text(f"Location: {booking_details['location']}"),
                ft.Text(f"Date: {booking_details['date']}"),
                ft.Text(f"Time: {booking_details['time']}"),
            ],
            tight=True,
        )
        
        global dialog
        dialog = ft.AlertDialog(
            title=ft.Text("Proceeding to Next Step"),
            content=dialog_content,
            actions=[
                ft.TextButton("OK", on_click=close_dialog),
            ],
        )
        
        page.dialog = dialog
        dialog.open = True
        page.update()

    def date_clicked(e, day):
        nonlocal selected_date
        clicked_date = datetime(current_display_date.year, current_display_date.month, day)
        if clicked_date.date() >= today:
            selected_date = clicked_date
            selected_date_text.value = clicked_date.strftime("%A, %B %d")
            booking_details["date"] = clicked_date.strftime("%A, %B %d")
            update_calendar()
            page.update()

    def update_calendar():
        while len(calendar_column.controls) > 2:
            calendar_column.controls.pop()

        cal = calendar.monthcalendar(current_display_date.year, current_display_date.month)
        month_text.value = current_display_date.strftime("%B %Y")
        
        for week in cal:
            week_row = ft.Row(spacing=0)
            for day in week:
                if day == 0:
                    day_cell = ft.Container(
                        width=60,
                        height=60,
                        padding=10,
                    )
                else:
                    date_to_check = datetime(current_display_date.year, current_display_date.month, day).date()
                    is_past = date_to_check < today
                    is_selected = (selected_date and 
                                 selected_date.year == current_display_date.year and
                                 selected_date.month == current_display_date.month and
                                 selected_date.day == day)
                    is_available = date_to_check >= today
                    
                    dot = ft.Container(
                        width=4,
                        height=4,
                        bgcolor="#000000" if is_available else "transparent",
                        border_radius=2,
                        visible=is_available and not is_selected
                    )
                    
                    day_content = ft.Column(
                        controls=[
                            ft.Text(
                                str(day),
                                size=16,
                                weight=ft.FontWeight.W_400,
                                color="#000000" if is_available else "#CCCCCC"
                            ),
                            dot
                        ],
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                    
                    day_cell = ft.Container(
                        content=day_content,
                        width=60,
                        height=60,
                        border_radius=5,
                        bgcolor="#5D4037" if is_selected else "#F5F5F5" if is_past else None,
                        on_click=None if is_past else lambda e, d=day: date_clicked(e, d),
                        padding=10,
                    )
                    
                    if is_selected:
                        day_content.controls[0].color = "white"
                
                week_row.controls.append(day_cell)
            calendar_column.controls.append(week_row)
        
        page.update()

    def previous_month(e):
        nonlocal current_display_date
        first_day_of_current_month = today.replace(day=1)
        first_day_of_target_month = (current_display_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        
        if first_day_of_target_month >= first_day_of_current_month:
            if current_display_date.month == 1:
                current_display_date = current_display_date.replace(year=current_display_date.year - 1, month=12)
            else:
                current_display_date = current_display_date.replace(month=current_display_date.month - 1)
            update_calendar()

    def next_month(e):
        nonlocal current_display_date
        if current_display_date.month == 12:
            current_display_date = current_display_date.replace(year=current_display_date.year + 1, month=1)
        else:
            current_display_date = current_display_date.replace(month=current_display_date.month + 1)
        update_calendar()

    def create_calendar():
        calendar_column.controls = [
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.CHEVRON_LEFT,
                        icon_size=24,
                        icon_color="#000000",
                        on_click=previous_month
                    ),
                    month_text,
                    ft.IconButton(
                        icon=ft.icons.CHEVRON_RIGHT,
                        icon_size=24,
                        icon_color="#000000",
                        on_click=next_month
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            day,
                            size=14,
                            weight=ft.FontWeight.W_400,
                            color="#000000"
                        ),
                        width=60,
                        height=40,
                        alignment=ft.alignment.center
                    )
                    for day in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
                ],
            ),
        ]
        
        update_calendar()
        return calendar_column

    def time_slot_clicked(e, time_container):
        for row in time_slots_grid.controls:
            for container in row.controls:
                container.bgcolor = "white"
                container.content.color = "black"
        
        time_container.bgcolor = "#5D4037"
        time_container.content.color = "white"
        booking_details["time"] = time_container.content.value
        page.update()

    def create_time_slots():
        global time_slots_grid
        time_slots_grid = ft.Column(spacing=10)
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
                        width=125,  # Increased from 120
                        height=50,  # Increased from 35
                        border=ft.border.all(2, "#DEDEDE"),
                        border_radius=5,
                        padding=10,
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
                        width=125,  # Increased from 120
                        height=50,  # Increased from 35
                        border=ft.border.all(2, "#DEDEDE"),
                        border_radius=5,
                        padding=10,
                        alignment=ft.alignment.center,
                        bgcolor="white",
                        on_click=lambda e, t=times[i + 1]: time_slot_clicked(e, e.control)
                    )
                )
            
            time_slots_grid.controls.append(row)
        
        return time_slots_grid

    # Create main layout
    main_content = ft.Row(
        controls=[
            # Calendar section
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Select a Date",
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
                    ],
                    spacing=20,
                ),
                padding=20,
            ),
            
            ft.VerticalDivider(width=1, color="#DEDEDE"),
            
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Select Time",
                            size=20,
                            weight=ft.FontWeight.BOLD
                        ),
                        create_time_slots(),
                    ],
                    spacing=20,
                ),
                padding=20,
                width=300,
            ),
            
            ft.VerticalDivider(width=1, color="#DEDEDE"),
            
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Booking Details",
                            size=20,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(booking_details["service"], size=16, weight=ft.FontWeight.W_500),
                                    ft.Text(booking_details["duration"], size=14),
                                    ft.Text(booking_details["location"], size=14),
                                ],
                                spacing=5,
                            ),
                            padding=ft.padding.only(top=10, bottom=20),
                        ),
                        ft.ElevatedButton(
                            "Next",
                            bgcolor="#5D4037",
                            color="white",
                            width=200,
                            height=40,
                            on_click=navigate_to_next_page
                        ),
                    ],
                    spacing=10,
                ),
                padding=20,
                width=250,
            ),
        ],
        spacing=0,
    )

    page.add(main_content)
    page.update()

ft.app(target=main)
