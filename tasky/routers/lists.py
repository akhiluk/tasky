from fastapi import Depends, status, HTTPException, APIRouter, Response
from tasky import crud, schemas, models, oauth2
from tasky.database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix = "/lists", tags = ["Lists"])

@router.get("/", response_model = List[schemas.TaskList], status_code = status.HTTP_200_OK)
def get_task_lists(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), skip: int = 0, limit: int = 10):
    if current_user is not None:
        task_lists = crud.get_task_lists(db, current_user, skip, limit)
        return task_lists
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")

@router.get("/{id}", response_model = schemas.TaskList, status_code = status.HTTP_200_OK)
def get_task_list(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if current_user is not None:
        task_list = crud.get_task_list(db, id, current_user)
        if task_list is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Task list not found.")
        return task_list
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")

@router.post("/", response_model = schemas.TaskList, status_code = status.HTTP_201_CREATED)
def create_task_list(task_list: schemas.TaskListCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if current_user is not None:
        task_list = crud.create_task_list(db = db, task_list = task_list, user = current_user)
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")
    return task_list

@router.put("/", response_model = schemas.TaskList, status_code = status.HTTP_200_OK)
def update_task_list(task_list: schemas.TaskListUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if current_user is not None:
        task_list = crud.update_task_list(db = db, task_list = task_list, user = current_user)
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")
    return task_list

@router.delete("/", status_code = status.HTTP_204_NO_CONTENT)
def delete_task_list(task_list: schemas.TaskListDelete, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if current_user is not None:
        db_task_list = crud.get_task_list(db, task_list.id, current_user)
        if db_task_list is not None:
            crud.delete_task_list(db, db_task_list.id)
            return Response(status_code = status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "List not found.")
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")    
