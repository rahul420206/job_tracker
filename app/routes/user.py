# app/routes/user.py
from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate
from app.models import user as user_model
from app.core import security
from app.dependencies import require_role

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", dependencies=[Depends(require_role(["admin"]))])
def create_user(user: UserCreate):
    existing_user = user_model.get_user_by_username(user.username)
    if existing_user:
        return {"error": "User already exists"}

    hashed_pw = security.hash_password(user.password)
    success = user_model.create_user(user.username, hashed_pw, user.role)
    if success:
        return {"message": "User created"}
    else:
        return {"error": "Failed to create user"}
