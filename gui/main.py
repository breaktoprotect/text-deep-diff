from nicegui import ui
from gui.layout import setup_layout

setup_layout()

ui.run(native=False, title="Text Deep Diff")
