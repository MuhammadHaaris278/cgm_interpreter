from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.api.endpoints import router
from app.config.loader import Config
from pathlib import Path

config = Config()

app = FastAPI(
    title=config.app_name,
    description="AI-Powered CGM Interpretation Service",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="ui"), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
async def serve_frontend():
    """Serve the main UI"""
    return FileResponse("ui/index.html")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "THYRA CGM Interpretation API"}