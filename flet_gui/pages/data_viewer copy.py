import flet as ft
import httpx
from icecream import ic

BASE_URL = "http://127.0.0.1:8000/api/v1/upload"

async def view(page: ft.Page):
    file_dropdown = ft.Dropdown(label="Uploaded File", options=[], width=400)
    explorer_section = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    filename_to_hash = {}
    page_state = {"file_hash": None}
    client = httpx.AsyncClient()

    async def load_uploaded_files():
        try:
            res = await client.get(f"{BASE_URL}/list")
            files = res.json().get("files", [])

            file_dropdown.options = []
            for f in files:
                filename = f["filename"]
                file_hash = f["file_hash"]
                filename_to_hash[filename] = file_hash
                file_dropdown.options.append(ft.dropdown.Option(text=filename))

            if files:
                first_filename = file_dropdown.options[0].text
                file_dropdown.value = first_filename
                page_state["file_hash"] = filename_to_hash[first_filename]
                ic("Selected file_hash:", page_state["file_hash"])
                await display_file_structure(page_state["file_hash"])
        except Exception as e:
            print("load_uploaded_files error:", e)

    async def display_file_structure(file_hash):
        explorer_section.controls.clear()
        try:
            res = await client.get(f"{BASE_URL}/{file_hash}/sheets")
            sheet_names = res.json().get("sheets", [])

            for sheet in sheet_names:
                col_res = await client.get(f"{BASE_URL}/{file_hash}/sheets/{sheet}/columns")
                columns = col_res.json().get("columns", []) if col_res.status_code == 200 else []

                explorer_section.controls.append(
                    ft.ExpansionTile(
                        title=ft.Text(sheet, weight="bold"),
                        subtitle=ft.Text(f"{len(columns)} columns"),
                        maintain_state=True,
                        controls=[
                            ft.Text(f"• {col}", size=12) for col in columns
                        ]
                    )
                )

            page.update()
        except Exception as e:
            print("display_file_structure error:", e)

    async def on_file_change(e):
        selected_filename = e.control.value
        file_hash = filename_to_hash.get(selected_filename, "")
        page_state["file_hash"] = file_hash
        ic("Manually selected file_hash:", file_hash)
        await display_file_structure(file_hash)

    file_dropdown.on_change = on_file_change

    await load_uploaded_files()

    return ft.Column([
        ft.Text("Uploaded File Structure", theme_style="headlineMedium"),
        file_dropdown,
        ft.Divider(),
        explorer_section
    ], expand=True)
