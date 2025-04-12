import flet as ft
import httpx
from icecream import ic

BASE_URL = "http://127.0.0.1:8000/api/v1/upload"


async def view(page: ft.Page):
    file_dropdown = ft.Dropdown(label="Uploaded File", options=[], width=400)
    explorer_section = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    filename_to_id = {}
    page_state = {"file_id": None}
    client = httpx.AsyncClient()

    async def load_uploaded_files():
        try:
            res = await client.get(f"{BASE_URL}/list")
            files = res.json().get("files", [])

            file_dropdown.options = []
            for f in files:
                filename = f["filename"]
                file_id = f["file_id"]
                filename_to_id[filename] = file_id
                file_dropdown.options.append(ft.dropdown.Option(text=filename))

            if files:
                first_filename = file_dropdown.options[0].text
                file_dropdown.value = first_filename
                page_state["file_id"] = filename_to_id[first_filename]
                ic("Selected file_id:", page_state["file_id"])
                await display_file_structure(page_state["file_id"])
        except Exception as e:
            print("load_uploaded_files error:", e)

    async def display_file_structure(file_id):
        explorer_section.controls.clear()
        try:
            res = await client.get(f"{BASE_URL}/{file_id}/sheets")
            sheet_names = res.json().get("sheets", [])

            for sheet in sheet_names:
                col_res = await client.get(
                    f"{BASE_URL}/{file_id}/sheets/{sheet}/columns"
                )
                columns = (
                    col_res.json().get("columns", [])
                    if col_res.status_code == 200
                    else []
                )

                explorer_section.controls.append(
                    ft.ExpansionTile(
                        title=ft.Text(sheet, weight="bold"),
                        subtitle=ft.Text(f"{len(columns)} columns"),
                        maintain_state=True,
                        controls=[
                            ft.DataTable(
                                columns=[
                                    ft.DataColumn(ft.Text(col)) for col in columns
                                ],
                                rows=[
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text("…")) for _ in columns
                                        ]
                                    )
                                ],
                                heading_row_height=40,
                                horizontal_margin=10,
                                divider_thickness=1,
                            )
                        ],
                    )
                )

            page.update()
        except Exception as e:
            print("display_file_structure error:", e)

    async def on_file_change(e):
        selected_filename = e.control.value
        file_id = filename_to_id.get(selected_filename, "")
        page_state["file_id"] = file_id
        ic("Manually selected file_id:", file_id)
        await display_file_structure(file_id)

    file_dropdown.on_change = on_file_change

    await load_uploaded_files()

    return ft.Column(
        [
            ft.Text("Uploaded File Structure", theme_style="headlineMedium"),
            file_dropdown,
            ft.Divider(),
            explorer_section,
        ],
        expand=True,
    )
