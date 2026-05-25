from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.api import api_router

# =========================
# PATHS
# =========================

ROOT_DIR = Path(__file__).resolve().parents[2]
STATIC_DIR = ROOT_DIR / "app" / "static"

# =========================
# APP
# =========================

app = FastAPI()

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# STATIC FILES (FIX REAL)
# =========================

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)

# =========================
# ROUTES
# =========================

app.include_router(api_router)