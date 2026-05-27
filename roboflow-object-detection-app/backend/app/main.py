from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.api import api_router

# =========================
# PATHS REALES
# =========================

BASE_DIR = Path(__file__).resolve().parent

STATIC_DIR = BASE_DIR / "static"

FRONTEND_DIR = BASE_DIR.parents[2] / "frontend"

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
# STATIC FILES
# =========================

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)

# =========================
# FRONTEND ASSETS
# =========================

app.mount(
    "/assets",
    StaticFiles(directory=str(FRONTEND_DIR / "assets")),
    name="assets"
)

# =========================
# API
# =========================

app.include_router(api_router)

# =========================
# FRONTEND
# =========================

@app.get("/")
async def root():
    return FileResponse(
        str(FRONTEND_DIR / "index.html")
    )

@app.get("/app.js")
async def js():
    return FileResponse(
        str(FRONTEND_DIR / "app.js")
    )

@app.get("/styles.css")
async def css():
    return FileResponse(
        str(FRONTEND_DIR / "styles.css")
    )