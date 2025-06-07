from langchain_ollama import ChatOllama

model = ChatOllama(model="mistral:instruct")

messages = [
    {
        "role": "system",
        "content": "You're a helpful assistant."
    },
    {
        "role": "user",
        "content": "Write a limerick about the Python programming language.",
    },
]

response = model.invoke(messages)
print(response.content)