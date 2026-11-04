from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import db_models

from models import (
    Task,
    TaskCreate,
    TaskUpdate,
    TaskDeleteResponse,
    UserCreate,
    User,
)

from crud import (
    find_task_by_id,
    get_all_tasks,
    create_task_db,
    delete_task_db,
    update_task_db,
    create_user_db,
    find_user_by_email,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API funcionando"}


@app.get("/tasks", response_model=list[Task])
def get_tasks(db: Session = Depends(get_db)):
    return get_all_tasks(db)


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = find_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada"
        )

    return task


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    return create_task_db(
        db,
        task.title,
        task.completed
    )


@app.delete("/tasks/{task_id}", response_model=TaskDeleteResponse)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    deleted_task = delete_task_db(db, task_id)

    if deleted_task is None:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada"
        )

    return {
        "message": "Tarea eliminada",
        "id": deleted_task.id,
        "title": deleted_task.title,
        "completed": deleted_task.completed
    }


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db)
):
    updated_task = update_task_db(
        db,
        task_id,
        task.title,
        task.completed
    )

    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada"
        )

    return updated_task


@app.post("/register", response_model=User, status_code=201)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = find_user_by_email(db, user.email)

    if existing_user is not None:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado"
        )

    return create_user_db(
        db,
        user.email,
        user.password
    )