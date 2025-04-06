from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api.v1.compare import router as compare_router
from app.api.v1.upload import router as upload_router
import gui.gui_main as gui_main

app = FastAPI()

app.include_router(compare_router, prefix="/api/v1")
app.include_router(upload_router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
def redirect_to_gui():
    return RedirectResponse(url="/gui")


gui_main.init(app)

if __name__ == "__main__":
    print(
        'Please start the app with the "uvicorn" command as shown in the start.sh script'
    )
