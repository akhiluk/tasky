from fastapi import Depends, status, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from tasky.database import get_db
from tasky import schemas, crud, oauth2, models
from typing import Optional, List

router = APIRouter(prefix = "/tasks", tags = ["Tasks"])

@router.get("/", response_model = List[schemas.Task], status_code = status.HTTP_200_OK)
def get_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), task_list: int = 0, skip: int = 0, limit: int = 10, show_completed: bool = False):
    if current_user is not None:
        tasks = crud.get_tasks(db, current_user, task_list, skip, limit, show_completed)
        return tasks
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")

@router.get("/{id}", response_model = schemas.Task, status_code = status.HTTP_200_OK)
def get_task(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if current_user is not None:
        task = crud.get_task(db, id, current_user)
        if task is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Task not found")
        return task
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")

@router.post("/", response_model = schemas.Task, status_code = status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    if current_user is not None:
        task = crud.create_task(db = db, task = task, user = current_user)
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")
    if task is None:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid List provided.")
    return task

@router.put("/", response_model = schemas.Task, status_code = status.HTTP_200_OK)
def update_task(task: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if current_user is not None:
        db_task = crud.get_task(db, task.id, current_user)
        if db_task is not None:
            updated_task = crud.update_task(db, task, current_user)
            if updated_task is not None:
                return updated_task
            else:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid list provided.")
        else:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Task not found")
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")
    
@router.delete("/", status_code = status.HTTP_204_NO_CONTENT)
def delete_task(task: schemas.TaskDelete, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if current_user is not None:
        db_task = crud.get_task(db, task.id, current_user)
        if db_task is not None:
            crud.delete_task(db, db_task.id)
            return Response(status_code = status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Task not found.")
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")