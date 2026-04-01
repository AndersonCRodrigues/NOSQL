from fastapi import APIRouter, Depends, HTTPException, status

from ..core.dependencies import get_task_service
from ..schemas.tasks import TaskCreate, TaskResponse, TaskUpdate
from ..services.tasks import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(service: TaskService = Depends(get_task_service)):
    return await service.get_all()


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, service: TaskService = Depends(get_task_service)):
    task = await service.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task não encontrada")
    return task


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(data: TaskCreate, service: TaskService = Depends(get_task_service)):
    return await service.create(data)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, data: TaskUpdate, service: TaskService = Depends(get_task_service)):
    task = await service.update(task_id, data)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task não encontrada")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, service: TaskService = Depends(get_task_service)):
    deleted = await service.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task não encontrada")
