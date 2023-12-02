import requests
import json
import os
from typing import List

from dotenv import load_dotenv
load_dotenv()

url = os.environ("LLM_API_URL")

def get_rag_query(query: str, documents: List[str]):
    context = "\n\n".join(documents)
    query = f"""{context}
    
Based on the information given above, answer the questions below:
{query}"""
    return query

def get_generation_prompt(messages, search_results=[]):
    chat_prompt = ""
    documents = [item["document"] for item in search_results]
    for i, message in enumerate(messages):
        # 대화 턴이 너무 긴 경우 최근 메시지만 사용
        # if i > 0 and i < len(messages) - 3:
        #     continue
        role = message["role"]
        content = message["content"]
        
        if i == len(messages) - 1:
            content = get_rag_query(content, documents)
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
            #"truncate": True,
            "repetition_penalty": 1.03,
            "details": False,
            "decoder_input_details": False,
            "stop": ["</s>"]
        }
    }
    with requests.post(url=url, json=data, stream=True) as response:
        generated_text = ""
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                try:
                    json_data = json.loads(chunk.decode('utf-8').lstrip('data:'))
                    token = json_data["token"]["text"]
                    generated_text = json_data["generated_text"]
                    yield token, generated_text
                except:
                    yield "", generated_text
                    
if __name__ == "__main__":
    
    sample_messages = [
        {"role": "user", "content": "Hi there!"},
        {"role": "user", "content": "Oh, Hello!"}
    ]
    
    prompt = get_generation_prompt(sample_messages)
    print(prompt)
    
    for chunk in generate(prompt):
        print(chunk)
