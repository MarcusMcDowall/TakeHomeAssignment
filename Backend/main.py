import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import timedelta

from user_Auth import login, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from AI_Logic import call_AI

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

class AIModel(BaseModel):
    prompt: str = Field()

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/login/")
async def loginEP(user_Data: LoginData):
    return login(user_Data.username, user_Data.password)

@app.post("/ai/")
async def ai_endpoint(data: AIModel, token: str = Depends(oauth2_scheme)):
    current_user = await get_current_user(token)  # make sure to await async
    response = call_AI(data.prompt, current_user)
    return {"response": response}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    result = login(form_data.username, form_data.password)
    if "error" in result:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": form_data.username, "user_id": result["User"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "Bearer"}
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)