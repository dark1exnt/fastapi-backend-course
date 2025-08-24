from fastapi import FastAPI, HTTPException, status
from typing import List
from pathlib import Path

from storage import JsonTasks, Task, TaskUpdate

app = FastAPI()
DATA_FILE = Path("data/tasks.json")
tasks_db = JsonTasks(DATA_FILE)



@app.get("/tasks", response_model=List[Task])
def get_tasks() -> List[Task]:
    return tasks_db.get_all()

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: Task) -> Task:
    return tasks_db.add(task)

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate) -> Task:
    return tasks_db.update(task_id, task_update)



@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> None:
    tasks_db.delete(task_id)