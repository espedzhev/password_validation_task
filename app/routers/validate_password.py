from app.validation import is_valid_password, evaluate_password_rules
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


@router.get("/rules")
async def get_rules():
    return DEFAULT_RULES


class PasswordRequest(BaseModel):
    password: str


@router.post("/validate")
async def validate_password(request: PasswordRequest):
    valid = is_valid_password(request.password)
    return {"valid": valid}


@router.post("/validate/rules")
async def validate_password_rules(request: PasswordRequest):
    rules_status = evaluate_password_rules(request.password)
    return {"rules": rules_status}
