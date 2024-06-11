from pydantic import BaseModel, EmailStr
import datetime
from typing import Union, List

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    email: EmailStr
    password: str

class User(UserBase):
    email: EmailStr
    created_at: datetime.datetime

    class Config:
        from_attributes = True

################################################################

class TaskBase(BaseModel):
    pass

class TaskCreate(TaskBase):
    title: str
    details: str
    list_id: int

class TaskUpdate(TaskBase):
    id: int
    title: Union[str, None]
    details: Union[str, None]
    is_completed: Union[bool, None] = False
    list_id: int

class TaskDelete(TaskBase):
    id: int

class Task(TaskBase):
    id: int
    title: str
    details: str
    is_completed: bool
    user: User
    list_id: int

    class Config:
        from_attributes = True

################################################################

class TaskListBase(BaseModel):
    pass

class TaskListCreate(TaskListBase):
    name: str

class TaskListUpdate(TaskListBase):
    id: int
    name: str

class TaskListDelete(TaskListBase):
    id: int

class TaskList(TaskListBase):
    id: int
    name: str
    tasks: List[Task]

################################################################

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None