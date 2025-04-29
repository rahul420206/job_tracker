from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate
from app.models import user as user_model
from app.core import security
from app.dependencies import require_role

router = APIRouter(prefix="/users", tags=["Users"])

# Only admin can create users
@router.post("/", dependencies=[Depends(require_role(["admin"]))])
def create_user(user: UserCreate):
    existing_user = user_model.get_user_by_username(user.username)
    if existing_user:
        return {"error": "User already exists"}

    hashed_password = security.get_password_hash(user.password)
    user_model.create_user(user.username, hashed_password, user.role)
    return {"message": f"User '{user.username}' created successfully"}

# Admins and recruiters can view all users (example route)
@router.get("/", dependencies=[Depends(require_role(["admin", "recruiter"]))])
def list_users():
    users = user_model.get_all_users()
    return {"users": users}

# Any authenticated user can view their profile
@router.get("/me")
def get_my_profile(user=Depends(require_role(["admin", "recruiter", "user"]))):
    return {"username": user["username"], "role": user["role"]}


def get_user_by_username(username: str):
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    return cursor.fetchone()
