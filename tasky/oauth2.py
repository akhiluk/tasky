import jwt
from jwt.exceptions import InvalidTokenError
import datetime
from tasky import crud, config
from tasky.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire_at = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire_at})

    encoded_jwt = jwt.encode(to_encode, key = SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        decoded_token = jwt.decode(jwt = token, key = SECRET_KEY, algorithms = [ALGORITHM])
        username = decoded_token.get("username")

        if username is None:
            raise credentials_exception
        
        return username
    except InvalidTokenError:
        raise credentials_exception
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentials.", headers = {"WWW-Authenticate": "Bearer"})

    username = verify_access_token(token, credentials_exception)

    db_user = crud.get_user(db, username)

    return db_user