from fastapi import APIRouter
from fastapi import Depends
from app import app_settings
import logging
from pydantic import BaseModel
import openai

openai.api_key = "sk-ijklmnopuvwx1234ijklmnopuvwx1234ijklmnop"
router = APIRouter(prefix=f"{app_settings.api_prefix}/llm", tags=["LLM"])
logger = logging.getLogger("llm")

class Prompt(BaseModel):
    prompt: str

@router.post("/chat")
async def chat(prompt: Prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt.prompt},
        ],
    )
    return {"response": response.choices[0].message['content']}

