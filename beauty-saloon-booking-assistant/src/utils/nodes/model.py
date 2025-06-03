from functools import lru_cache

from langchain_ollama import ChatOllama
from src.utils.tools.tools import tools


@lru_cache(maxsize=4)
def get_model():
    model = ChatOllama(
        model="mistral",
        temperature=0.0,
    )
    model = model.bind_tools(tools)
    return model