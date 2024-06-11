from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from tasky.database import get_db
from tasky import crud, utils, schemas, oauth2

router = APIRouter(tags = ["Authentication"])

@router.post("/login", response_model = schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_credentials.username)

    if db_user is None:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid credentials provided.")
    if utils.verify(user_credentials.password, db_user.password):
        access_token = oauth2.create_access_token(data = {'username': user_credentials.username})

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid credentials provided.")