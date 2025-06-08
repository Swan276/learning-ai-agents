from langgraph.graph import MessagesState

from utils.nodes.model import get_model
from utils.prompts.assistant_prompts import PRIMARY_INSTRUCTION


def booking_assistant(state: MessagesState):
    model = get_model()
    return {"messages": [model.invoke([PRIMARY_INSTRUCTION] + state["messages"])]}