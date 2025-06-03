from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_ollama import  ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langgraph.graph import MessagesState, StateGraph

llm = ChatOllama(
    model="mistral",
    temperature=0.0,
)


sys_msg = SystemMessage(content="You are a beauty saloon booking assistant tasked with greeting customers and helping them book their appointment, with desired service, specialist, date and time. ")
def booking_assistant(state: MessagesState):
   return {"messages": [llm.invoke([sys_msg] + state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("booking_assistant", booking_assistant)

builder.add_edge(START, "booking_assistant")

memory = MemorySaver()

graph = builder.compile(checkpointer=memory)

def run_booking_assistant():
    config = {"configurable": {"thread_id": "1"}}
    state = graph.invoke({"messages": [HumanMessage("Hello")]}, config)
    response = get_ai_message(state)
    print(response)

    while True:
        print("\n\n-------------------------")
        user_input = input("Ask your question (q to quit):").strip()
        print("\n\n")
        if user_input == "q":
            break
        state = graph.invoke({"messages": [HumanMessage(user_input)]}, config)
        response = get_ai_message(state)
        print(response)

def get_ai_message(state: MessagesState):
    messages = state.get("messages")
    if messages and len(messages) > 0:
        return messages[-1].content
    return ""

if __name__ == "__main__":
    run_booking_assistant()

