from fastapi import FastAPI, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from itertools import count


app = FastAPI()


class Task(BaseModel):
    id: Optional[int] = None
    title: str
    status: str = "to do"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None


tasks_db: List[Task] = []

_id_seq = count(1)


@app.get("/tasks", response_model=List[Task])
def get_tasks() -> List[Task]:
    return tasks_db

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: Task) -> Task:
    task.id = next(_id_seq)
    tasks_db.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate) -> Task:
    for task in tasks_db:
        if task.id == task_id:
            if task_update.title is not None:
                task.title = task_update.title
            if task_update.status is not None:
                task.status = task_update.status

            return task
    raise HTTPException(status_code=404, detail="Task not found")



@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> None:
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Task not found")