from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Union
from authentication import authenticate_user


"""
class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
    email: Union[str, None] = None
    disabled: Union[bool, None] = None



class UserInDB(User):
    hashed_password: str
"""


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX30XePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}



app = FastAPI()
app.title = "API Security"

# This class receives a token as parameter, so what we are saying here is that we have an endpoint called "token" which will return the required information.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/", tags=["Root"])
def welcome():
    return HTMLResponse(""" 
            <h1 style="text-align: center;">Favorite Songs</h1>
            <article style="display:flex; justify-content:center">
                <ul>
                    <li>Ciudad de la Furia - Soda Stereo</li>
                    <li>When I was your man - Bruno Mars</li>
                    <li>Scars 2020 - Papa Roach</li>
                </ul>
            </article>""")


@app.get("/users/me", tags=["Users"])
def user(token: str = Depends(oauth2_scheme)): # Depends is a function which will be executed when we use this endpoint.
    print(token)
    return "Hey User!"



@app.post("/token", tags=["Token"])
def login(login_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, login_data.username, login_data.password)
    print(user)
    return {"access_token": "Tostadas", "token_type": "bearer"}







