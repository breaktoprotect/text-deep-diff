import flet as ft
import asyncio
from flet_gui.pages import upload, data_viewer

nav_map = {
    0: ("Upload", upload.view),
    1: ("Data Viewer", data_viewer.view),
}

async def main(page: ft.Page):
    page.title = "text-deep-diff"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.START

    body = ft.Container(expand=True, padding=20)

    async def on_nav_change(e):
        label, render_fn = nav_map[e.control.selected_index]
        body.content = await render_fn(page)
        page.update()

    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=True,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.UPLOAD_FILE, label="Upload"),
            ft.NavigationRailDestination(icon=ft.Icons.TABLE_ROWS, label="Data Viewer"),
        ],
        on_change=on_nav_change,
    )

    body.content = await nav_map[0][1](page)

    page.add(ft.Row([nav_rail, body], expand=True))

asyncio.run(ft.app_async(target=main))
