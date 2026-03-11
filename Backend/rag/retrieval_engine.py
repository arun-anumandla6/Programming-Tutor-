from typing import List
from langchain_community.vectorstores import Chroma


class RetrievalEngine:

    COLLECTIONS = {
        "python": "python_index",
        "java": "java_index",
        "go": "go_index"
    }

    def __init__(self, persist_directory: str, embedding_function):
        self.persist_directory = persist_directory
        self.embedding_function = embedding_function
        self._collections = {}

    def _get_collection(self, language: str):
        language = language.lower().strip()

        if language not in self.COLLECTIONS:
            raise ValueError(f"Unsupported language: {language}")

        if language not in self._collections:
            self._collections[language] = Chroma(
                collection_name=self.COLLECTIONS[language],
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_function,
            )

        return self._collections[language]

    def retrieve(self, language: str, query: str) -> str:

        if not language or not query:
            return ""

        collection = self._get_collection(language)

        docs = collection.similarity_search(query, k=4)

        contexts: List[str] = []

        for doc in docs:
            if hasattr(doc, "page_content") and doc.page_content:
                contexts.append(doc.page_content.strip())

        return "\n\n".join(contexts)