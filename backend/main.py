from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.recommendation_routes import router as recommendation_router

app = FastAPI(
    title="SmartPlate AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    recommendation_router
)


@app.get("/")
def root():
    return {
        "message": "SmartPlate AI API is running"
    }