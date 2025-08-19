import uvicorn
from fastapi import Body
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import timedelta

from user_Auth import login, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user, get_user_by_id, update_password, delete_user
from AI_Logic import call_AI

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#useful initialization for a more "live" startup and reload
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

# creating models for later use
class LoginData(BaseModel):
    username: str = Field()
    password: str = Field()

class AIModel(BaseModel):
    prompt: str = Field()

class Token(BaseModel):
    access_token: str
    token_type: str

#all FastAPI pathing and routes created below
@app.post("/login/")
async def loginEP(user_Data: LoginData):
    return login(user_Data.username, user_Data.password)

@app.post("/ai/")
async def ai_endpoint(data: AIModel, token: str = Depends(oauth2_scheme)):
    current_user = await get_current_user(token)  # make sure to await async otherwise cant run in time = error
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
    # If login is successful, create a JWT token
    return {"access_token": access_token, "token_type": "Bearer"}
    #returns users token to allow user for other request types

#basic crud routing from user_Auth
@app.get("/users/me/")
async def read_current_user(current_user: dict = Depends(get_current_user)):
    return get_user_by_id(current_user.user_id)

@app.put("/users/me/password/")
async def change_password(new_password: str = Body(...), current_user: dict = Depends(get_current_user)):
    return update_password(current_user.user_id, new_password)

@app.delete("/users/me/delete/")
async def remove_user(current_user: dict = Depends(get_current_user)):
    return delete_user(current_user.user_id
)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)