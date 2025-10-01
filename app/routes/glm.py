import openai
import logging
import os

from fastapi import APIRouter
from fastapi import Depends
from app.utils.current_user import get_current_user
from fastapi import HTTPException, status
from typing import List
from app import app_settings
from pydantic import BaseModel

# Konfigurasi GLM-4.5
GLM_API_KEY = os.getenv("GLM_API_KEY", "your-glm-api-key")  # Ganti dengan API key GLM Anda
GLM_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"  # Base URL untuk GLM-4.5

# Inisialisasi client OpenAI untuk GLM-4.5
client = openai.OpenAI(
    api_key=GLM_API_KEY,
    base_url=GLM_BASE_URL
)

router = APIRouter(prefix=f"{app_settings.api_prefix}/glm", tags=["GLM"])
logger = logging.getLogger("llm")


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: float = 0.7
    max_tokens: int = 1000
    model: str = "glm-4"  # Model default GLM-4


class ChatResponse(BaseModel):
    response: str
    model: str
    usage: dict


# Endpoint GLM-4.5
@app.post("/chat", response_model=ChatResponse)
async def chat_with_glm(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    try:
        # Format pesan untuk GLM-4.5
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Panggil GLM-4.5
        response = client.chat.completions.create(
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        # Ekstrak respons
        response_content = response.choices[0].message.content
        usage_info = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        
        return ChatResponse(
            response=response_content,
            model=response.model,
            usage=usage_info
        )
    except openai.APIError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"GLM API Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
