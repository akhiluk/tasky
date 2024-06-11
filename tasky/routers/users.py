from fastapi import APIRouter, Depends, status, HTTPException
from tasky import crud, schemas
from tasky.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix = "/users", tags = ["Users"])

@router.post("/", response_model = schemas.User, status_code = status.HTTP_200_OK)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    return db_user