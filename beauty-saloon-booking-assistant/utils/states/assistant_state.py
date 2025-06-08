from langchain_core.messages import BaseMessage
from typing import TypedDict, Annotated

from langgraph.graph import add_messages

from utils.states.customer_info import CustomerInfo

class AssistantState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]