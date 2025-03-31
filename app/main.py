from fastapi import FastAPI
from app.api.v1.compare import router as compare_router
from app.api.v1.upload import router as upload_router

app = FastAPI()

app.include_router(compare_router, prefix="/api/v1")
app.include_router(upload_router, prefix="/api/v1")
