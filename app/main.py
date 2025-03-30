from fastapi import FastAPI
from app.api.v1.compare import router as compare_router

app = FastAPI()

app.include_router(compare_router, prefix="/api/v1")
