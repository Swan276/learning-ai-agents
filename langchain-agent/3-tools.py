import os
import functools

import requests
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool

load_dotenv()

@tool
def get_weather(latitude: float,longitude: float) -> dict:
    """Get current temperature for provided coordinates in Celsius."""
    print("getting weather")
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]

tools = [
    {
        "function": {
            "name": "get_weather",
            "description": "Get current temperature for provided coordinates in celsius.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
            "strict": True,
        },
        "type": "function",
    }
]

names_to_functions = {
    'get_weather': functools.partial(get_weather),
}

system_prompt = "You are a helpful weather assistant."

messages = [
    SystemMessage(system_prompt),
    HumanMessage("Could you get the current temperature for Dublin, Ireland. It's coordinates are approximately 53.2910794,-6.36603."),
]

class WeatherResponse(BaseModel):
    temperature: float = Field(
        description="The current temperature in celsius for the given location."
    )
    response: str = Field(
        description="A natural language response to the user's question."
    )

api_key = os.environ["GEMINI_API_KEY"]

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai", api_key=api_key)

model = model.bind_tools([get_weather])

ai_message = model.invoke(messages)

print(ai_message.tool_calls)

messages.append(ai_message)

for tool_call in ai_message.tool_calls:
    selected_tool = {"get_weather": get_weather}[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

print(messages)

ai_response = model.invoke(messages)

print(ai_response)