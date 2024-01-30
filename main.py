import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from fake_database import fake_users_db
from authentication import authenticate_user, get_user, create_access_token, Token, TokenData


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))



app = FastAPI()
app.title = "API Security"

# This class receives a token as parameter, so what we are saying here is that we have an endpoint called "token" which will return the required information.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



async def get_current_user(token: str = Depends(oauth2_scheme)):
    """ Decode the received token, verify it, and return the current user. If the token is invalid, return an HTTP error right away. """
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username == None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, token_data.username)

    if user == None:
        raise credentials_exception

    return user



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
def user(current_user: str = Depends(get_current_user)): # Depends is a function which will be executed when we use this endpoint.

    return current_user



@app.post("/token", tags=["Token"])
def login(login_data: OAuth2PasswordRequestForm = Depends()):
    
    user = authenticate_user(fake_users_db, login_data.username, login_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Wrong username or password", headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")





