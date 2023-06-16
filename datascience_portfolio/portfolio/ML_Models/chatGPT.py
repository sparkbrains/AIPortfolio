import openai
import os
from dotenv import load_dotenv
load_dotenv() 
openai.api_key = os.getenv('CHATGPT_KEY')
def get_completion_from_messages(message):
    chat_models = "gpt-3.5-turbo" 
    messages = [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}]
    
    response = openai.ChatCompletion.create(
        model=chat_models,
        messages=messages
    )
    return str(response.choices[0].message['content'])




