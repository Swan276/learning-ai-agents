from langchain_core.messages import HumanMessage
from langchain_ollama import OllamaLLM
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_openai import  ChatOpenAI

@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing simple mathematical operations."""
    print("calculator tool is called")
    return f"The sum of {a} and {b} is {a + b}"

def main():
    model = ChatOpenAI(
        model="llama3.2",
        api_key="ollama",
        base_url="http://localhost:11434/v1",
    )

    tools = [calculator]

    agent_executor = create_react_agent(model, tools)

    print("Welcome! I am your personal assistant. Type 'q' to quit.")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "q":
            break

        print("\nAssistant: ", end="")
        for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()

if __name__ == "__main__":
    main()
