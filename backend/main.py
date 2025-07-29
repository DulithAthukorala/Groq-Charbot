import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()


class Message(BaseModel):
    messages: List[Dict[str, str]]  # ✅ Proper structure: list of {role, content} dicts


@app.post("/chat")
def chat(msg: Message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": msg.messages
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    reply = response.json()["choices"][0]["message"]["content"]
    return {"response": reply}
