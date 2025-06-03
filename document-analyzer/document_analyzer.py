from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from database import get_db_instance

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

class DocumentAnalyzer:
    def __init__(self):
        self.db = get_db_instance()
        self.model = ChatOllama(model="mistral")

    def ask(self, question: str):
        # Search the DB.
        results = self.db.similarity_search_with_relevance_scores(question, k=3)
        print(results)
        if len(results) == 0 or results[0][1] < 0.3:
            return "Sorry! I am unable to find any relevant information relating to question."

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=question)
        print(prompt)

        response_text = self.model.invoke(prompt)

        sources = [doc.metadata.get("source", None) for doc, _score in results]
        formatted_response = f"Response: {response_text}\nSources: {sources}"
        return formatted_response