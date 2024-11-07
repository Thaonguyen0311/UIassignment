import flet as ft
from home import HomePage
from about import AboutPage
from service import ServicePage
from contact import ContactPage

def main(page: ft.Page):
    page.title = "Beauty Salon"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Page content container
    content_container = ft.Container(expand=True, padding=20)

    # Function to switch between pages
    def switch_page(tab_index):
        if tab_index == 0:
            content_container.content = HomePage()
        elif tab_index == 1:
            content_container.content = AboutPage()
        elif tab_index == 2:
            content_container.content = ServicePage()
        elif tab_index == 3:
            content_container.content = ContactPage()
        page.update()

    # Initially display the home page content
    switch_page(0)

    # Create Tabs component
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Home"),
            ft.Tab(text="About"),
            ft.Tab(text="Service"),
            ft.Tab(text="Contact"),
        ],
        on_change=lambda e: switch_page(e.control.selected_index),
        expand=True
    )

    # Put Tabs in a Container and set an appropriate height
    header_container = ft.Container(
        content=ft.Column(
            [tabs],
            alignment=ft.MainAxisAlignment.CENTER,  # Vertically centered
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Horizontally centered
        ),
        height=100,  # Set to an appropriate height
        padding=ft.Padding(top=5, right=0, bottom=5, left=0),  # Set padding
        bgcolor=ft.colors.RED_50,  # Set background color
    )

    # Page layout
    page.add(ft.Column([header_container, content_container], expand=True))
# ft.app(target=main, port=8080)

ft.app(target=main)









