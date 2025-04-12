from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request
)
from sqlalchemy.orm import Session

from mspt.apps.mspt import (
    schemas,
    crud,
)
from mspt.apps.users import models as user_models
from mspt.settings.database import get_db
from mspt.settings.security import (
    get_current_active_user
)

router = APIRouter()
db_session = Session()


@router.get("/task", response_model=schemas.TaskPaginated)
def read_tasks(
        *,
        db: Session = Depends(get_db),
        request: Request,
        page: int = 1,
        size: int = 20,
        shared: bool = False,
        sort_on: str = 'uid',
        sort_order: str = 'desc',
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Retrieve tasks.
    """
    tasks = crud.task.get_paginated_multi(
        db, 
        request=request,
        page=page, 
        size=size, 
        owner_uid=current_user.uid,
        shared=shared,
        sort_on=sort_on,        
        sort_order=sort_order
    )
    return tasks


@router.post("/task", response_model=schemas.Task)
def create_task(
        *,
        db: Session = Depends(get_db),
        task_in: schemas.TaskCreate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Create new task.
    """
    task_in.owner_uid = current_user.uid
    task = crud.task.create(db, obj_in=task_in)
    return task


@router.put("/task/{task_uid}", response_model=schemas.Task)
def update_task(
        *,
        db: Session = Depends(get_db),
        task_uid: int,
        task_in: schemas.TaskUpdate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Update an task.
    """
    task = crud.task.get(db, uid=task_uid)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="This task does not exist in the system",
        )
    task = crud.task.update(db, db_obj=task, obj_in=task_in)
    return task


@router.delete("/task/{task_uid}", response_model=schemas.TaskDelete)
def delete_task(
        *,
        db: Session = Depends(get_db),
        task_uid: int,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Delete an task.
    """
    task = crud.task.get(db, uid=task_uid)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="This task does not exist in the system",
        )
    task = crud.task.remove(db, uid=task_uid)
    return task