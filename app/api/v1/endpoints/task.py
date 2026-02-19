from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskResponse
from app.models.user import User

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
    "/",
    response_model=TaskResponse,
    summary="Create a new task",
    description="Create a new task for the currently authenticated user."
)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    return service.create_task(
        title = task.title,
        description = task.description,
        user_id = current_user.id
    )


@router.get(
    "/",
    response_model=list[TaskResponse],
    summary="Get all tasks for the authenticated user",
    description="Retrieve a list of all tasks that belong to the currently authenticated user."
)
def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    return service.get_tasks(current_user.id)

@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Task not found"},
    },
    summary="Get a specific task",
    description="Retrieve a specific task by its ID that belongs to the currently authenticated user."
)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    task = service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Task not found"
        )
    return task

@router.delete(
    "/{task_id}",
    summary="Delete a specific task",
    description="Delete a specific task by its ID that belongs to the currently authenticated user."
)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    result = service.delete_task(task_id, current_user.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Task not found"
        )
    return {"message": "Task deleted"}