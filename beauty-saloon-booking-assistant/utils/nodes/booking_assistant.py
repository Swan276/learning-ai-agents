from utils.nodes.model import get_model
from utils.prompts.assistant_prompts import primary_assistant_prompt
from utils.states.assistant_state import AssistantState


def booking_assistant(state: AssistantState):
    model = get_model()
    return {"messages": [model.invoke([primary_assistant_prompt] + state["messages"])]}