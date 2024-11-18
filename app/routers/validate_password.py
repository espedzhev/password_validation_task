from app.validation import is_valid_password
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

router = APIRouter()


@router.post("/validate")
async def validate_password(request: Request):
    data = await request.json()
    password = data.get("password", "")
    valid = is_valid_password(password)
    return JSONResponse({"password": password, "valid": valid})


@router.get("/",response_class=HTMLResponse)
async def home():
    with open("app/templates/index.html") as f:
        return f.read()
