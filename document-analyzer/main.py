from document_analyzer import DocumentAnalyzer

def chat():
    analyzer = DocumentAnalyzer()

    while True:
        print("Ask me questions about the documents (q to quit)")
        question = input("Question: ").strip()
        if question == "q":
            break
        response = analyzer.ask(question)
        print(response)

if __name__ == "__main__":
    chat()