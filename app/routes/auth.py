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

# app/routes/auth.py

from fastapi import APIRouter, HTTPException, Depends, Form
from app.core.security import verify_password, create_access_token
from app.database import get_db
from datetime import timedelta

router = APIRouter()

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(
        data={"sub": user["username"], "role": user.get("role", "user")},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}
