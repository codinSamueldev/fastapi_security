from fastapi import HTTPException
from pydantic import BaseModel
from typing import Union
from fake_database import fake_users_db


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
    email: Union[str, None] = None
    disabled: Union[bool, None] = None



class UserInDB(User):
    hashed_password: str



def fake_hash_password(password: str):
    return "fakehashed" + password



def get_user(db, username):
    """ 
    Verify if user exist in the Database. If exists return user, if not return empty string.
    """
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data) # UserInDB parameters will be filled with username information.

    return []


def authenticate_user(login_data):
    user_dict = fake_users_db.get(login_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password.")

    user = UserInDB(**user_dict) # UserInDB(**user_dict) means: Pass the keys and values of the user_dict directly as key-value arguments.
    hashed_password = fake_hash_password(login_data.password)
    if hashed_password != user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password.")

    # return user




