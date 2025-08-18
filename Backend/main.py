import uvicorn
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from user_Auth import login

app = FastAPI()

origins = [
    "https://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login/")
async def loginEP(username: str = Form(...), password: str = Form(...)):
    return login(username, password)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)