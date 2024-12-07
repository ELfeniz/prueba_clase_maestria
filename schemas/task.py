from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Schema for creating a new task
class TaskCreate(BaseModel):
    user_id: int = Field(..., description="ID of the user creating the task")
    task_name: str = Field(..., max_length=255, description="Name of the task")
    description: Optional[str] = Field(None, max_length=500, description="Description of the task")
    date_due: datetime = Field(..., description="Due date for the task")

# Schema for updating the status of a task
class TaskUpdateStatus(BaseModel):
    status: bool = Field(..., description="Updated status of the task")

# Schema for displaying task details
class TaskResponse(BaseModel):
    task_id: int
    user_id: int
    task_name: str
    description: Optional[str]
    date_due: datetime
    status: bool