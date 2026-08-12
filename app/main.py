from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI PetCare Assistant API",
    description="Petco Summer Hackathon 2026",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

@app.get("/api/v1/health", summary="Health Check", description="Returns the current health status of the API.", tags=["System"])
def health_check():
    return {"status": "ok"}
