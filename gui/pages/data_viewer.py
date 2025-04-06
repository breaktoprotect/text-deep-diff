# gui/pages/data_viewer.py

from nicegui import ui
import requests

API_BASE = "http://localhost:8000/api/v1"


def render():
    ui.label("📁 Uploaded Files")

    container = ui.column().classes("w-full")

    # def fetch_files():
    #     container.clear()
    #     try:
    #         response = requests.get(f"{API_BASE}/upload/list")
    #         if response.ok:
    #             files = response.json().get("files", [])
    #             for f in files:
    #                 ui.label(f'{f["filename"]} ({f["file_hash"]})', parent=container)
    #         else:
    #             ui.notify("Failed to fetch files", type="negative")
    #     except Exception as e:
    #         ui.notify(f"Error: {str(e)}", type="negative")

    # fetch_files()
