# ------------------setting up openai API key setup (chatbot)------------------
import os
import openai
import datetime
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


chat_log = []
n_remembered_post = 2


if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', "exit", "bye"]:
            break

        chat_log.append({'role': 'user', 'content': user_input})

        if len(chat_log) > n_remembered_post:
            del chat_log[:len(chat_log)-n_remembered_post]

        response = chat_with_gpt(chat_log)
        
        dtm_timestamp = datetime.datetime.now()
        dtm_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("Chatbot:", response)
        chat_log.append({'role': "assistant", 'content': response})
        cursor.execute("INSERT INTO Content (user_id, prompt, response, Created_timestamp) VALUES (?, ?, ?, ?);", (user_id, user_input, response, dtm_timestamp))
        connection.commit()

connection.close()
