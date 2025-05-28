from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """
You are an expert in answering questions about a pizza restaurant.

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def handle_conversation():
    while True:
        print("\n\n-------------------------")
        question = input("Ask you question (q to quit): ")
        print("\n\n")
        if question == "q":
            break

        reviews = retriever.invoke(question)
        response = chain.invoke({"reviews": reviews, "question": question})
        print(response)

if __name__ == "__main__":
    handle_conversation()
