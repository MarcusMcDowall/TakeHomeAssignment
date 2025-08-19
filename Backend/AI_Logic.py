# ------------------setting up openai API key setup (chatbot)------------------
import os
import openai
from datetime import datetime
import sqlite3

from dotenv import load_dotenv
from user_Auth import login

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


connection = sqlite3.connect('LocalDB/localDB.db')
cursor = connection.cursor()

if __name__ == "__main__":
    user_id = login()

def chat_with_gpt(chat_log):
    response = openai.ChatCompletion.create(model='gpt-5-nano', messages=chat_log)
    return response.choices[0].message.content.strip()

def call_AI(prompt: str, current_user):
    user_id = current_user.user_id


    chat_log = [{'role': 'user', 'content': prompt}]
    response_text = chat_with_gpt(chat_log)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect('LocalDB/localDB.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Content (user_id, prompt, response, Created_timestamp) VALUES (?, ?, ?, ?);",
            (user_id, prompt, response_text, timestamp)
        )

        conn.commit()

    return response_text