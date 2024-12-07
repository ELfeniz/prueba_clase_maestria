from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.db_models import Task
from schemas.task import TaskCreate, TaskUpdateStatus, TaskResponse
from typing import List

def create_task(db: Session, task: TaskCreate) -> TaskResponse:
    new_task = Task(
        user_id=task.user_id,
        task_name=task.task_name,
        description=task.description,
        date_due=task.date_due,
        status=False  # Default status is False (incomplete)
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks_by_user(db: Session, user_id: int) -> List[TaskResponse]:
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this user")
    return tasks

def update_task_status(db: Session, task_id: int) -> TaskResponse:
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = not(task.status)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}
