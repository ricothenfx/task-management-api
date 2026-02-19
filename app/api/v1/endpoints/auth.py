from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.auth_service import AuthService
from app.schemas.user import UserRegister, UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
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


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    service = AuthService(db)
    return service.login(
        email = form_data.username,
        password = form_data.password
    )