from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()
app.title = "API Security"

# This class receives a token as parameter, so what we are saying here is that we have an endpoint called "token" which will return the required information.
oauth2_scheme = OAuth2PasswordBearer("/token")


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
    return "Hey User!"


