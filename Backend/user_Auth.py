# ------------------ setting up the user authentication page ------------------
import sqlite3
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# -------- creating models -----------
class TokenData(BaseModel):
    username: str | None = None

class UserInDB(BaseModel):
    username: str
    user_id: int
    disabled: bool = False


# -------- Functionality ------------
def login(username: str, password: str):
    connection = sqlite3.connect('LocalDB/localDB.db')
    cursor = connection.cursor()

    cursor.execute("SELECT user_id, userpsw FROM User WHERE username=?", (username,))#fetches data(password) related to the given username
    row = cursor.fetchone()

    #----------Sign In/Create Acc --------
    if row:
        user_id, hashed_psw = row
        if not pwd_context.verify(password, hashed_psw):#verifies plain password to username related hashed psw
            connection.close()
            return {"error": "Invalid credentials"}
        message = f"Welcome back user: {username}!"
    else: #if username isnt found it creates new account saving details to sqlite db
        hashed_psw = pwd_context.hash(password)
        cursor.execute("INSERT INTO User (username, userpsw) VALUES (?, ?);", (username, hashed_psw))
        connection.commit()
        user_id = cursor.lastrowid #copy row id of newest save
        message = f"a new account has been created for: {username}!"

    connection.close()
    
    access_token = create_access_token(#setting up creating a token for user upon succesful auth
        data={"sub": username, "user_id": user_id}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    return {"User": user_id, "Authenticator": message, "access_token": access_token, "token_type": "bearer"}

# ----------- creating and setting paramaters for token ---------
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# ------------------ Get current user ------------------
async def get_current_user(token: str = Depends(oauth_2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")

        if username is None or user_id is None:
            raise credentials_exception
        return UserInDB(username=username, user_id=user_id)
    except JWTError:
        raise credentials_exception

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user

#---------- basic Crud Operations (Create is already complete for accounts) ------------

#Read
def get_user_by_id(user_id: int):
    connection = sqlite3.connect('LocalDB/localDB.db')
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, username FROM User WHERE user_id=?", (user_id,))
    Usertb = cursor.fetchone()
    cursor.execute("SELECT * from Content WHERE user_id=?", (user_id,))
    Contenttb = cursor.fetchall()
    
    connection.close()

    if Usertb:
        return {"user_id": Usertb[0], "username": Usertb[1], "user_content": Contenttb}
    
    return None

#Update
def update_password(user_id: int, new_password: str):
    hashed_psw = pwd_context.hash(new_password)
    connection = sqlite3.connect('LocalDB/localDB.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE User SET userpsw=? WHERE user_id=?", (hashed_psw, user_id))
    connection.commit()
    connection.close()

    return {"message": "you successfully changed your accounts password, please restart"}

#Delete
def delete_user(user_id: int):
    connection = sqlite3.connect('LocalDB/localDB.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM User WHERE user_id=?", (user_id,))
    connection.commit()
    connection.close()

    return {"message": "Your Account has been removed"}