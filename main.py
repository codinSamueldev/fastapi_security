from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()
app.title = "API Security"


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
            </article>
            """)


