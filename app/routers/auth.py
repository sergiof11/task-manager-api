from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import find_user_by_email
from app.database import get_db
from app.schemas import User, UserLogin
from app.security import verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login", response_model=User)
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
        )

    return user