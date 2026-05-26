from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.api import api_router

# =========================
# PATHS
# =========================

ROOT_DIR = Path(__file__).resolve().parents[2]

STATIC_DIR = ROOT_DIR / "backend" / "app" / "static"

FRONTEND_DIR = ROOT_DIR / "frontend"

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
# FRONTEND FILES
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
# FRONTEND ROUTE
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