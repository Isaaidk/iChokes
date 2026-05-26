from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.api import api_router

# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parents[2]

FRONTEND_DIR = BASE_DIR / "frontend"

STATIC_DIR = BASE_DIR / "backend" / "app" / "static"

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
# API ROUTES
# =========================

app.include_router(api_router)

# =========================
# FRONTEND INDEX
# =========================

@app.get("/")
async def root():

    return FileResponse(
        FRONTEND_DIR / "index.html"
    )

# =========================
# FRONTEND FILES
# =========================

@app.get("/{file_name}")
async def frontend_files(
    file_name: str
):

    file_path = FRONTEND_DIR / file_name

    if file_path.exists():

        return FileResponse(file_path)

    return {
        "error": "File not found"
    }