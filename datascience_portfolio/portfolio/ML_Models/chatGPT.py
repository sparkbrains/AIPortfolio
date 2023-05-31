import openai
openai.api_key = "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"

def get_completion_from_messages(message):
    chat_models = "gpt-3.5-turbo" 
    messages = [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}]
    
    response = openai.ChatCompletion.create(
        model=chat_models,
        messages=messages
    )
    
    return str(response.choices[0].message['content'])



