from langchain_core.tools import tool


@tool
def lookup_guidelines(query: str) -> str:
    """Consult the company guidelines to see available services, booking policies and guidelines.
    Use this before making any booking changes performing other 'write' events."""
    # docs = retriever.query(query, k=2)
    # return "\n\n".join([doc["page_content"] for doc in docs])