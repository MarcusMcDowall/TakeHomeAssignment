# login.py
import sqlite3

def login():
    connection = sqlite3.connect('LocalDB/localDB.db')
    cursor = connection.cursor()

    username = input("What is your username: ")
    password = input("What is your password: ")

    # Check if user already exists
    cursor.execute("SELECT user_id FROM User WHERE username=? AND userpsw=?", (username, password))
    row = cursor.fetchone()

    if row:  # User exists
        user_id = row[0]
        print(f"Welcome back, {username}! (user_id={user_id})")
    else:  # New user → create entry
        cursor.execute("INSERT INTO User (username, userpsw) VALUES (?, ?);", (username, password))
        connection.commit()
        user_id = cursor.lastrowid
        print(f"New account created for {username}! (user_id={user_id})")

    connection.close()
    return user_id

if __name__ == "__main__":
    uid = login()
    print("Your user_id is:", uid)
