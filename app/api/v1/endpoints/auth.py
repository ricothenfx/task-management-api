from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.auth_service import AuthService
from app.schemas.user import UserRegister, UserLogin

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    summary="Register a new user",
    description="Create a new user account with the provided email and password."
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    service = AuthService(db)
    service.register(
        email = user.email,
        password = user.password
    )
    return {"message": "User registered successfully"}


@router.post(
    "/login",
    summary="User login",
    description="Authenticate user and return a JWT access token."
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    service = AuthService(db)
    return service.login(
        email = form_data.username,
        password = form_data.password
    )