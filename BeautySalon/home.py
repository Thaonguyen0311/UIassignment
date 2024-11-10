import flet as ft
import os

def HomePage():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_path = os.path.join(current_dir, "assets")
    image_path = os.path.join(assets_path, "picture1.png")
    
    return ft.Stack(
        [
            # Background image with full path
            ft.Image(
                src=image_path,
                width=1920,  
                height=1080,  
                fit=ft.ImageFit.COVER,  
                repeat=ft.ImageRepeat.NO_REPEAT
            ),
            
            # Container for text and button (positioned at right)
            ft.Container(
                content=ft.Column(
                    [
                        # Four lines of text
                        ft.Text(
                            "Are you Ready",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLACK,
                        ),
                        ft.Text(
                            "for a new",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLACK,
                        ),
                        ft.Text(
                            "& better",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLACK,
                        ),
                        ft.Text(
                            "you",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLACK,
                        ),
                        
                        # Add some spacing between text and button
                        ft.Container(height=20),
                        
                        # Book appointment button
                        ft.TextButton(
                            text="Book an appointment",
                            style=ft.ButtonStyle(
                                color={
                                    "": ft.colors.WHITE,
                                    "hovered": ft.colors.PINK_50,
                                },
                                bgcolor={
                                    "": ft.colors.PINK,
                                    "hovered": ft.colors.PINK_900,
                                },
                            ),
                            width=200,
                            height=50,
                        ),
                    ],
                    spacing=5,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                ),
                padding=ft.padding.only(right=100, top=400),
                alignment=ft.alignment.top_right,
            ),
        ],
        width=1920,
        height=1080,
    )