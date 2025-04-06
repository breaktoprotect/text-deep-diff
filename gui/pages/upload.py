# gui/pages/upload.py

from nicegui import ui
import requests

API_BASE = "http://localhost:8000/api/v1"


def render():
    ui.label("📤 Upload XLSX File").classes("text-xl font-bold")

    # upload_result = ui.column().classes("mt-4")
    #
    # def handle_upload(e):
    #     file = e.content
    #     filename = e.name
    #     response = requests.post(
    #         f"{API_BASE}/upload",
    #         files={
    #             "file": (
    #                 filename,
    #                 file,
    #                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    #             )
    #         },
    #     )
    #     if response.ok:
    #         ui.notify("✅ Upload successful!")
    #         show_uploaded_files()
    #     else:
    #         try:
    #             msg = response.json().get("detail", "Unknown error")
    #         except Exception:
    #             msg = response.text
    #         ui.notify(f"❌ Upload failed: {msg}", type="negative")

    # ui.upload(
    #     auto_upload=True, on_upload=handle_upload, label="Upload .xlsx/.xls file"
    # ).props("accept=.xlsx,.xls").classes("mt-2")

    # def show_uploaded_files():
    #     upload_result.clear()
    #     resp = requests.get(f"{API_BASE}/upload/list")
    #     if resp.ok:
    #         files = resp.json().get("files", [])
    #         with upload_result:
    #             if not files:
    #                 ui.label("No files uploaded yet.")
    #                 return
    #             ui.label("📂 Uploaded Files:").classes("text-lg mt-4")
    #             for file in files:
    #                 ui.label(f'{file["filename"]} ({file["file_hash"]})')
    #     else:
    #         ui.notify("❌ Failed to fetch uploaded files", type="negative")

    # show_uploaded_files()
