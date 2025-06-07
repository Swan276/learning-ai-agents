from langchain_ollama import ChatOllama
from pydantic import BaseModel

model = ChatOllama(model="mistral:instruct")

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

messages = [
    {
        "role": "system",
        "content": "Extract the event information."
    },
    {
        "role": "user",
        "content": "Alice and Bob are going to a science fair on Friday.",
    },
]

response = model.with_structured_output(CalendarEvent).invoke(messages)
print(response)
