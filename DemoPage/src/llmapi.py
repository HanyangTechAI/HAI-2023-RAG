import requests
import json

url = "http://localhost:40101/generate_stream"

def get_generation_prompt(messages):
    chat_prompt = ""
    for i, message in enumerate(messages):
        if i > 0 and i < len(messages) - 3:
            continue
        role = message["role"]
        content = message["content"]
        chat_prompt += f"<|{role}|>\n"
        chat_prompt += f"{content}</s> \n"
    chat_prompt += "<|assistant|>\n"
    return chat_prompt

def generate(prompt: str, max_new_tokens: int = 1024):
    """
    A generator that yields data from a streaming HTTP request.
    """
    data = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "details": False,
            "decoder_input_details": False,
            "stop": ["</s>"]
        }
    }
    with requests.post(url=url, json=data, stream=True) as response:
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                try:
                    json_data = json.loads(chunk.decode('utf-8').lstrip('data:'))
                    yield json_data["token"]["text"], json_data["generated_text"]
                except:
                    yield "", None
if __name__ == "__main__":
    
    sample_messages = [
        {"role": "user", "content": "Hi there!"},
        {"role": "user", "content": "Oh, Hello!"}
    ]
    
    prompt = get_generation_prompt(sample_messages)
    print(prompt)
    
    for chunk in generate(prompt):
        print(chunk)
