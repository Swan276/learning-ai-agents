from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import START
from langgraph.graph import MessagesState, StateGraph

llm = ChatOpenAI(
    model="mistral",
    api_key="ollama",
    base_url="http://localhost:11434/v1",
    temperature=0.0,
)

sys_msg = SystemMessage(content="You are a beauty saloon booking assistant tasked with greeting customers and helping them book their appointment, with desired service, specialist, date and time. ")
def booking_assistant(state: MessagesState):
   return {"messages": [llm.invoke([sys_msg] + state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("booking_assistant", booking_assistant)

builder.add_edge(START, "booking_assistant")

graph = builder.compile()

