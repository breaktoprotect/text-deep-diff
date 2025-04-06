from nicegui import ui


@ui.page("/export")
def render():
    with ui.column().classes("p-4"):
        ui.label("Output page (placeholder)").classes("text-h5")
        ui.label("This will display results or output of your analysis in future.")
