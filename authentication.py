from fastapi import HTTPException
from pydantic import BaseModel
from typing import Union
from passlib.context import CryptContext


context = CryptContext(schemes=["bcrypt"], deprecated="auto") # CryptContext will help us to validate user hashed_password.


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
    email: Union[str, None] = None
    disabled: Union[bool, None] = None



class UserInDB(User):
    hashed_password: str



def get_user(db, username):
    """ 
    Verify if user exist in the Database. If exists return user, if not return empty string.
    """
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data) # UserInDB parameters will be filled with username information.

    return []


def verify_password(plain_password, hashed_password):
    """ 
    Validate if password is correct or not.
    """
    return context.verify(plain_password, hashed_password) # verify method will return a boolean value.



def authenticate_user(db, username, password):
    user = get_user(db, username)

    if not user:
        raise HTTPException(status_code=404, detail="User or password not found...", headers={"WWW-Authenticate": "Bearer"})

    if verify_password(password, user.hashed_password): # If password is True, then won't enter the if. Otherwise, raise error.
        return user
    """
    else:
        raise HTTPException(status_code=404, detail="User or password not found...", headers={"WWW-Authenticate": "Bearer"})"""




