from nicegui import ui
from gui.pages import export, upload, compare, data_viewer, analysis


# def setup_layout():
#     with ui.tabs().classes("w-full") as tabs:
#         upload_tab = ui.tab("Upload")
#         data_viewer_tab = ui.tab("Data Viewer")
#         compare_tab = ui.tab("Compare")
#         output_tab = ui.tab("Output")

#     with ui.tab_panels(tabs, value=upload_tab).classes("w-full"):
#         with ui.tab_panel(upload_tab):
#             upload.render()
#         with ui.tab_panel(data_viewer_tab):
#             data_viewer.render()
#         with ui.tab_panel(compare_tab):
#             compare.render()
#         with ui.tab_panel(output_tab):
#             output.render()


# * new layout
def setup_layout():
    with ui.splitter(value=30).classes("w-full h-512") as splitter:
        with splitter.before:
            with ui.tabs().props("vertical").classes("w-full") as tabs:
                upload_tab = ui.tab("Upload", icon="upload")
                data_viewer_tab = ui.tab("View Data", icon="dataset")
                analysis_tab = ui.tab("Analysis", icon="analytics")
                export_tab = ui.tab("Export Data", icon="download")
        with splitter.after:
            with ui.tab_panels(tabs, value=upload_tab).props("vertical").classes(
                "w-full h-full"
            ):
                with ui.tab_panel(upload_tab):
                    upload.render()
                with ui.tab_panel(data_viewer_tab):
                    data_viewer.render()
                with ui.tab_panel(export_tab):
                    export.render()
                with ui.tab_panel(analysis_tab):
                    analysis.render()
