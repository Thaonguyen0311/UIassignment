import flet as ft
from home import HomePage
from about import AboutPage
from service import ServicePage
from contact import ContactPage

def main(page: ft.Page):
    page.title = "Beauty Salon"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    def route_change(e):
        page.views.clear()
        
        if page.route == "/" or page.route == "":
            page.views.append(
                ft.View(
                    "/",
                    [
                        make_nav_bar(),
                        HomePage()
                    ]
                )
            )
        elif page.route == "/about":
            page.views.append(
                ft.View(
                    "/about",
                    [
                        make_nav_bar(),
                        AboutPage()
                    ]
                )
            )
        elif page.route == "/service":
            page.views.append(
                ft.View(
                    "/service",
                    [
                        make_nav_bar(),
                        ServicePage()
                    ]
                )
            )
        elif page.route == "/contact":
            page.views.append(
                ft.View(
                    "/contact",
                    [
                        make_nav_bar(),
                        ContactPage()
                    ]
                )
            )
        
        page.update()
    
    def make_nav_bar():
        return ft.Container(
            content=ft.Row(
                [
                    ft.TextButton(
                        text="Home",
                        on_click=lambda _: page.go("/"),
                        style=ft.ButtonStyle(
                            color={
                                "": ft.colors.BLACK,
                                "hovered": ft.colors.PINK
                            },
                        )
                    ),
                    ft.TextButton(
                        text="About",
                        on_click=lambda _: page.go("/about"),
                        style=ft.ButtonStyle(
                            color={
                                "": ft.colors.BLACK,
                                "hovered": ft.colors.PINK
                            },
                        )
                    ),
                    ft.TextButton(
                        text="Service",
                        on_click=lambda _: page.go("/service"),
                        style=ft.ButtonStyle(
                            color={
                                "": ft.colors.BLACK,
                                "hovered": ft.colors.PINK
                            },
                        )
                    ),
                    ft.TextButton(
                        text="Contact",
                        on_click=lambda _: page.go("/contact"),
                        style=ft.ButtonStyle(
                            color={
                                "": ft.colors.BLACK,
                                "hovered": ft.colors.PINK
                            },
                        )
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=ft.colors.RED_50,
            padding=10,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.colors.RED_100))
        )
    
    # 设置路由变化监听
    page.on_route_change = route_change
    
    # 初始化显示首页
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)