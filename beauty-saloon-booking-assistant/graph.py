import uuid
from typing import Iterator

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph, MessagesState
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from utils.nodes.booking_assistant import booking_assistant
from utils.tools.tools import tools

load_dotenv()

class BookingAssistantAgent:
    def __init__(self, use_memory_checkpoint=True):
        self.graph = self.build_graph(use_memory_checkpoint)
        self._config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    @staticmethod
    def build_graph(use_memory_checkpoint: bool) -> CompiledStateGraph:
        builder = StateGraph(MessagesState)
        builder.add_node("booking_assistant", booking_assistant)
        builder.add_node("tools", ToolNode(tools))

        builder.add_edge(START, "booking_assistant")
        builder.add_conditional_edges("booking_assistant", tools_condition, ["tools", END])
        builder.add_edge("tools", "booking_assistant")

        if use_memory_checkpoint:
            memory = MemorySaver()
            return builder.compile(checkpointer=memory)
        else:
            return builder.compile()

    def invoke_stream(self, message: str) -> Iterator[str]:
        for msg, metadata in self.graph.stream(
                {"messages": [HumanMessage(message + " /no_think")]},
                self._config,
                stream_mode="messages",
        ):
            yield msg.content

graph = BookingAssistantAgent(use_memory_checkpoint=False).graph
