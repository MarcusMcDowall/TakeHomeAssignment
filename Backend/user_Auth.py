# login.py
import sqlite3
import os
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def login(username: str, password: str):
    connection = sqlite3.connect('LocalDB/localDB.db')
    cursor = connection.cursor()

    # Check if user already exists
    cursor.execute("SELECT user_id FROM User WHERE username=? AND userpsw=?", (username, password))
    row = cursor.fetchone()

    if row:  # User exists
        user_id = row[0]
        message = f"Welcome back, {username}!"
    else:  # New user → create entry
        cursor.execute("INSERT INTO User (username, userpsw) VALUES (?, ?);", (username, password))
        connection.commit()
        user_id = cursor.lastrowid
        message = f"New account created for {username}!"

    connection.close()
    return {"User": user_id, "Authenticator": message}
