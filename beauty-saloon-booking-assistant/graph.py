import re
import uuid
from typing import Iterator

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from utils.nodes.booking_assistant import booking_assistant
from utils.states.assistant_state import AssistantState
from utils.tools.tools import tools

class BookingAssistantAgent:
    def __init__(self, use_memory_checkpoint=True):
        self.graph = self.build_graph(use_memory_checkpoint)
        self._config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    @staticmethod
    def build_graph(use_memory_checkpoint: bool) -> CompiledStateGraph:
        builder = StateGraph(AssistantState)
        builder.add_node("booking_assistant", booking_assistant)
        builder.add_node("tools", ToolNode(tools))

        builder.add_edge(START, "booking_assistant")
        builder.add_conditional_edges("booking_assistant", tools_condition)
        builder.add_edge("tools", "booking_assistant")

        if use_memory_checkpoint:
            memory = MemorySaver()
            return builder.compile(checkpointer=memory)
        else:
            return builder.compile()

    def invoke_stream(self, message: str) -> Iterator[str]:
        removed_think = False
        think_count = 2
        for msg, metadata in self.graph.stream(
                {"messages": [HumanMessage(message + " /no_think")]},
                self._config,
                stream_mode="messages",
        ):
            # for qwen3 only
            if not removed_think:
                think_count -= len(re.findall(r"</?think>", msg.content))
                if think_count < 1:
                    removed_think = True
                yield re.sub(r"</?think>", "", msg.content).strip()
            else:
                yield msg.content

graph = BookingAssistantAgent(use_memory_checkpoint=False).graph
