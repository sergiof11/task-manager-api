from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import find_user_by_email
from app.database import get_db
from app.dependencies import get_current_user
from app.models import UserDB
from app.schemas import Token, User, UserLogin
from app.security import create_access_token, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login", response_model=Token)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    user = find_user_by_email(db, credentials.email)

    if user is None or not verify_password(
        credentials.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=User)
def get_me(
    current_user: UserDB = Depends(get_current_user),
):
    return current_user
