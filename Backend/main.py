import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

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

class LoginData(BaseModel):
    username: str = Field()
    password: str = Field()

@app.post("/login/")
async def loginEP(user_Data: LoginData):
    return login(user_Data.username, user_Data.password)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)