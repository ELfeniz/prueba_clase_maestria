from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.task import TaskCreate, TaskUpdateStatus, TaskResponse
from controllers.task import create_task, get_tasks_by_user, update_task_status, delete_task
from typing import List

router_tasks = APIRouter()

@router_tasks.post("/tasks/", response_model=TaskResponse)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)

@router_tasks.get("/tasks/user/{user_id}", response_model=List[TaskResponse])
def get_user_tasks(user_id: int, db: Session = Depends(get_db)):
    return get_tasks_by_user(db, user_id)

@router_tasks.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, db: Session = Depends(get_db)):
    return update_task_status(db, task_id)

@router_tasks.delete("/tasks/{task_id}")
def delete_task_route(task_id: int, db: Session = Depends(get_db)):
    return delete_task(db, task_id)
