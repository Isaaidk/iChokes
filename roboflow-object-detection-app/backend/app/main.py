from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.api import api_router

# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parents[2]

BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"

STATIC_DIR = BACKEND_DIR / "app" / "static"

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
# CREATE FOLDERS
# =========================

(STATIC_DIR / "uploads").mkdir(
    parents=True,
    exist_ok=True
)

(STATIC_DIR / "outputs").mkdir(
    parents=True,
    exist_ok=True
)

# =========================
# STATIC FILES
# =========================

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)

# =========================
# FRONTEND ASSETS
# =========================

ASSETS_DIR = FRONTEND_DIR / "assets"

if ASSETS_DIR.exists():

    app.mount(
        "/assets",
        StaticFiles(directory=str(ASSETS_DIR)),
        name="assets",
    )

# =========================
# API ROUTES
# =========================

app.include_router(api_router)

# =========================
# FRONTEND ROUTES
# =========================

INDEX_FILE = FRONTEND_DIR / "index.html"


@app.get("/")
async def root():

    if INDEX_FILE.exists():

        response = FileResponse(INDEX_FILE)

        # 🔥 EVITA CACHE EN CELULARES
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, "
            "proxy-revalidate, max-age=0"
        )

        return response

    return {
        "message": "Frontend not found"
    }


@app.get("/app.js")
async def app_js():

    js_file = FRONTEND_DIR / "app.js"

    response = FileResponse(
        js_file,
        media_type="application/javascript"
    )

    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, "
        "proxy-revalidate, max-age=0"
    )

    return response


@app.get("/styles.css")
async def styles_css():

    css_file = FRONTEND_DIR / "styles.css"

    response = FileResponse(
        css_file,
        media_type="text/css"
    )

    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, "
        "proxy-revalidate, max-age=0"
    )

    return response