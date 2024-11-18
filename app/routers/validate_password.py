from app.validation import is_valid_password
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["Password Validation"])

DEFAULT_RULES = {
    "min_length": 8,
    "require_uppercase": True,
    "require_lowercase": True,
    "require_digit": True,
    "require_underscore": True,
}


@router.get("api/v1/rules")
async def get_rules():
    return DEFAULT_RULES


class PasswordRequest(BaseModel):
    password: str


@router.post("/validate")
async def validate_password(request: PasswordRequest):
    """
    Returns the overall validity of the password
    """
    password = request.password
    valid = is_valid_password(password)
    return {"password": password, "valid": valid}


@router.post("/validate/rules")
async def validate_password_rules(request: PasswordRequest):
    """
    Returns the detailed rule validation for the password
    """
    password = request.password
    rules_status = is_valid_password(password, detailed=True)
    return {"password": password, "rules": rules_status}
