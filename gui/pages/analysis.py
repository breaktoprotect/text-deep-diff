from nicegui import ui


@ui.page("/analysis")
def render():
    with ui.column().classes("p-4"):
        ui.label("Analysis page (placeholder)").classes("text-h5")
        ui.label(
            "This will allow running different types of analysis on uploaded data."
        )
