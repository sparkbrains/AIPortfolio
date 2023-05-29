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



