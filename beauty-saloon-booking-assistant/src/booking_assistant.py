import uuid

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from src.utils.nodes.booking_assistant import booking_assistant
from src.utils.states.assistant_state import AssistantState
from src.utils.tools.tools import tools

builder = StateGraph(AssistantState)
builder.add_node("booking_assistant", booking_assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "booking_assistant")
builder.add_conditional_edges("booking_assistant",tools_condition)
builder.add_edge("tools", "booking_assistant")

memory = MemorySaver()

graph = builder.compile(checkpointer=memory)
# graph = builder.compile()

def run_booking_assistant():
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    # state = graph.invoke({"messages": [HumanMessage("Hello")]}, config)
    for msg, metadata in graph.stream(
            {"messages": [HumanMessage("Hello")]},
            config,
            stream_mode="messages",
    ):
        print(msg.content, end="")

    while True:
        print("\n-------------------------")
        user_input = input("Chat (q to quit): ").strip()
        if user_input == "q":
            break
        # state = graph.invoke({"messages": [HumanMessage(user_input)]}, config)
        for msg, metadata in graph.stream(
                {"messages": [HumanMessage(user_input)]},
                config,
                stream_mode="messages",
        ):
            print(msg.content, end="")
        print()

if __name__ == "__main__":
    run_booking_assistant()

