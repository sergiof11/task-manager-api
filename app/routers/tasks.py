from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import (
    create_task_db,
    delete_task_db,
    find_task_by_id,
    get_all_tasks,
    update_task_db,
)
from app.database import get_db
from app.dependencies import get_current_user
from app.models import UserDB
from app.schemas import Task, TaskCreate, TaskDeleteResponse, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[Task])
def get_tasks(db: Session = Depends(get_db)):
    return get_all_tasks(db)


@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = find_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada",
        )

    return task


@router.post("", response_model=Task, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    return create_task_db(
        db,
        task.title,
        task.completed,
        current_user.id,
    )


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
):
    updated_task = update_task_db(
        db,
        task_id,
        task.title,
        task.completed,
    )

    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada",
        )

    return updated_task


@router.delete("/{task_id}", response_model=TaskDeleteResponse)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    deleted_task = delete_task_db(db, task_id)

    if deleted_task is None:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada",
        )

    return {
        "message": "Tarea eliminada",
        "id": deleted_task.id,
        "title": deleted_task.title,
        "completed": deleted_task.completed,
    }