# app/routes/auth.py

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models import user as user_model
from app.schemas.user import UserCreate
from app.core import security

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register_user(user: UserCreate):
    existing_user = user_model.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = security.hash_password(user.password)
    success = user_model.create_user(user.username, hashed_pw, user.role)

    if not success:
        raise HTTPException(status_code=500, detail="Could not create user")
    return {"message": "User registered successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_model.get_user_by_username(form_data.username)
    if not user or not security.verify_password(form_data.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = security.create_access_token({"sub": user['username'], "role": user['role']})
    return {"access_token": token, "token_type": "bearer"}
