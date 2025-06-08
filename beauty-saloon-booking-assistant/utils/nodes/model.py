import os
from functools import lru_cache

from langchain.chat_models import init_chat_model
from utils.tools.tools import tools

@lru_cache(maxsize=4)
def get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    return init_chat_model(
        "gemini-2.0-flash",
        model_provider="google_genai",
        api_key=api_key
    ).bind_tools(tools)
