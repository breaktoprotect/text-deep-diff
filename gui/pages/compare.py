# gui/pages/compare.py

from nicegui import ui


@ui.page("/compare")
def render():
    with ui.column():
        ui.label("Compare Sentences").classes("text-h5")

        sentence1 = ui.textarea(
            label="Sentence List 1", placeholder="Enter one sentence per line"
        )
        sentence2 = ui.textarea(
            label="Sentence List 2", placeholder="Enter one sentence per line"
        )
        model_select = ui.select(
            ["all-MiniLM-L6-v2", "paraphrase-MiniLM-L12-v2"], label="Model"
        )

        def compare_sentences():
            sents1 = [s.strip() for s in sentence1.value.splitlines() if s.strip()]
            sents2 = [s.strip() for s in sentence2.value.splitlines() if s.strip()]
            model = model_select.value

            if len(sents1) != len(sents2):
                ui.notify("Lists must have the same length", type="warning")
                return

            import requests

            response = requests.post(
                "http://localhost:8000/api/v1/compare",
                json={"sentences1": sents1, "sentences2": sents2, "model_name": model},
            )

            if response.ok:
                ui.notify("Similarity computed!")
                results = response.json().get("similarity_scores", [])
                for i, score in enumerate(results):
                    ui.label(f"Pair {i+1}: {score:.4f}")
            else:
                ui.notify(f"Error: {response.text}", type="negative")

        ui.button("Compare", on_click=compare_sentences)
