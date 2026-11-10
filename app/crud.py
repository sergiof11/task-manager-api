from sqlalchemy.orm import Session

from app.models import TaskDB, UserDB
from app.security import hash_password


def get_all_tasks(db: Session):
    return db.query(TaskDB).all()


def find_task_by_id(db: Session, task_id: int):
    return db.query(TaskDB).filter(TaskDB.id == task_id).first()


def create_task_db(
    db: Session,
    title: str,
    completed: bool,
    user_id: int,
):
    task = TaskDB(
        title=title,
        completed=completed,
        user_id=user_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def update_task_db(db: Session, task_id: int, title: str, completed: bool):
    task = find_task_by_id(db, task_id)

    if task is None:
        return None

    task.title = title
    task.completed = completed

    db.commit()
    db.refresh(task)

    return task


def delete_task_db(db: Session, task_id: int):
    task = find_task_by_id(db, task_id)

    if task is None:
        return None

    db.delete(task)
    db.commit()

    return task


def create_user_db(db: Session, email: str, password: str):
    user = UserDB(
        email=email,
        hashed_password=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def find_user_by_email(db: Session, email: str):
    return db.query(UserDB).filter(UserDB.email == email).first()


def find_user_by_id(db: Session, user_id: int):
    return db.query(UserDB).filter(UserDB.id == user_id).first()
