from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
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
)


@router.get("", response_model=list[Task])
def get_tasks(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    completed: bool | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    return get_all_tasks(
        db,
        current_user.id,
        skip,
        limit,
        completed,
    )


@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    task = find_task_by_id(
        db,
        task_id,
        current_user.id,
    )

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
    task_id: Annotated[int, Path(gt=0)],
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    updated_task = update_task_db(
        db,
        task_id,
        task.title,
        task.completed,
        current_user.id,
    )

    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada",
        )

    return updated_task


@router.delete("/{task_id}", response_model=TaskDeleteResponse)
def delete_task(
    task_id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    deleted_task = delete_task_db(
        db,
        task_id,
        current_user.id,
    )

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