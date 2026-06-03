from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="API de Tarefas (CRUD)")

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class Task(TaskCreate):
    id: int

todo_list: List[Task] = []
id_counter = 1


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    global id_counter
    
    task_data = task_in.model_dump()
    new_task = Task(id=id_counter, **task_data)
    
    todo_list.append(new_task)
    id_counter += 1
    return new_task

@app.get("/tasks", response_model=List[Task])
def get_all_tasks():
    return todo_list

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in todo_list:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task_in: TaskCreate):
    for index, task in enumerate(todo_list):
        if task.id == task_id:
            task_data = updated_task_in.model_dump()
            updated_task = Task(id=task_id, **task_data)
            todo_list[index] = updated_task
            return updated_task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for index, task in enumerate(todo_list):
        if task.id == task_id:
            todo_list.pop(index)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=4000, reload=True)