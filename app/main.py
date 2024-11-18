import os

from app.routers import validate_password
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(validate_password.router)

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)
