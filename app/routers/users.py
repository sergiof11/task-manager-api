from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import create_user_db, find_user_by_email
from app.database import get_db
from app.models import User, UserCreate

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/register", response_model=User, status_code=201)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = find_user_by_email(db, user.email)

    if existing_user is not None:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado",
        )

    return create_user_db(
        db,
        user.email,
        user.password,
    )