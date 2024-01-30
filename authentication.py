import os
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Union
from dotenv import load_dotenv
from passlib.context import CryptContext
from fake_database import fake_users_db


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class Token(BaseModel):
    """ Define a Pydantic Model that will be used in the token endpoint for the response. """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None



class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
    email: Union[str, None] = None
    disabled: Union[bool, None] = None



class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Create a PassLib "context". This is what will be used to hash and verify passwords.



def fake_hash_password(password: str):
    return "fakehashed" + password


def verify_password(plain_password, hashed_password):
    """ Verify if a received password matches the hash stored. Returns boolean value. """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)



def get_user(db, username):
    """ 
    Verify if user exist in the Database. If exists return user, if not return empty string.
    """
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data) # UserInDB parameters will be filled with username information.

    return []



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """ 
    function to generate a new access token. 
    Params:
        data: a dictionary containing the data that you want to encod into the access token.
        expires_delta: an optional parameter of type timedelta that represents the expiration time of the token. If not provided, the default expiration time is set to 15 minutes.
    """
    to_encode = data.copy() # This is done to avoid modifying the original data.
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt




def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user




