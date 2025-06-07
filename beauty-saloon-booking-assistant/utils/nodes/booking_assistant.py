from langgraph.constants import END
from langgraph.graph import MessagesState

from utils.nodes.model import get_model
from utils.prompts.assistant_prompts import PRIMARY_INSTRUCTION


def booking_assistant(state: MessagesState):
    model = get_model()
    return {"messages": [model.invoke([PRIMARY_INSTRUCTION] + state["messages"])]}

def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END