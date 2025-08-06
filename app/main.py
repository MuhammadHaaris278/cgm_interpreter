from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.config.loader import Config

config = Config()

app = FastAPI(
    title=config.app_name,
    description="AI-Powered CGM Interpretation Service",
    version="1.0.0"
)

# Optional: allow local frontend apps to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount core API routes
app.include_router(router)