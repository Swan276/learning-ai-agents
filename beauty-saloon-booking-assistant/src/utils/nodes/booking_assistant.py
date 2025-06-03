from src.utils.nodes.model import get_model
from src.utils.prompts.assistant_prompts import primary_assistant_prompt
from src.utils.states.assistant_state import AssistantState


def booking_assistant(state: AssistantState):
    model = get_model()
    return {"messages": [model.invoke([primary_assistant_prompt] + state["messages"])]}