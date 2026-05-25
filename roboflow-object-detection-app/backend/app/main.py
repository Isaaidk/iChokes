from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from app.api.api import api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

app.include_router(api_router)

@app.get("/")
async def root():

    return {
        "status": "running"
    }