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

# app/routes/users.py (or main.py)

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.database import get_db
import pymysql

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")
    role = payload.get("role")  # if you're encoding role into token

    return {"username": username, "role": role}
