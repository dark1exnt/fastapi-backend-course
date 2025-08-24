from dataclasses import dataclass
from typing import List, Optional
from pydantic import BaseModel
import requests


class Task(BaseModel):
    id: Optional[str] = None
    title: str
    status: str = "to do"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None


@dataclass
class MockApiConfig:
    api_url: str
    resource: str = "tasks"


class MockApiTasks:
    def __init__(self, cfg: MockApiConfig, timeout_sec: float = 10.0):
        self._cfg = cfg
        self._timeout = timeout_sec
        self._session = requests.Session()

    def _collections_url(self) -> str:
        return f"{self._cfg.api_url.rstrip('/')}/{self._cfg.resource}"
    
    def _item_url(self, task_id: str) -> str:
        return f"{self._collections_url().rstrip('/')}/{task_id}"
    
    def get_all(self) -> List[Task]:
        response = self._session.get(self._collections_url(), timeout=self._timeout)
        response.raise_for_status()
        data = response.json()
        return [Task(**task) for task in data]
    
    def get_by_id(self, task_id: str) -> Task:
        response = self._session.get(self._item_url(task_id), timeout=self._timeout)
        if response.status_code == 404:
            raise KeyError("Task not found")
        response.raise_for_status()
        return Task(**response.json())

    def add(self, task_in: Task) -> Task:
        payload = task_in.model_dump(exclude={"id"})
        response = self._session.post(self._collections_url(), json=payload, timeout=self._timeout)
        response.raise_for_status()
        return Task(**response.json())
    
    def update(self, task_id: str, task_update: TaskUpdate) -> Task:
        payload = task_update.model_dump(exclude_none=True)
        if not payload:
            return self.get_by_id(task_id)
        
        response = self._session.put(self._item_url(task_id), json=payload, timeout=self._timeout)
        if response.status_code == 404:
            raise KeyError("Task not found")
        response.raise_for_status()
        return Task(**response.json())
    
    def delete(self, task_id: str) -> None:
        response = self._session.delete(self._item_url(task_id), timeout=self._timeout)
        if response.status_code == 404:
            raise KeyError("Task not found")
        response.raise_for_status()