import flet as ft
import httpx
import os

UPLOAD_URL = "http://127.0.0.1:8000/api/v1/upload"


async def view(page: ft.Page):
    output = ft.Column()
    file_picker = ft.FilePicker()

    async def upload_file(path, name):
        try:
            async with httpx.AsyncClient() as client:
                with open(path, "rb") as f:
                    files = {
                        "file": (
                            name,
                            f,
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                    }
                    res = await client.post(UPLOAD_URL, files=files)

            if res.status_code == 200:
                output.controls.append(ft.Text(f"✅ Uploaded: {name}"))
            else:
                output.controls.append(ft.Text(f"❌ Upload failed: {res.status_code}"))
        except Exception as e:
            output.controls.append(ft.Text(f"❌ Error: {e}"))
        page.update()

    async def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            await upload_file(file.path, file.name)

    file_picker.on_result = on_file_picked

    return ft.Column(
        [
            file_picker,
            ft.ElevatedButton(
                "Choose Excel File",
                on_click=lambda _: file_picker.pick_files(allowed_extensions=["xlsx"]),
            ),
            ft.Divider(),
            output,
        ]
    )
