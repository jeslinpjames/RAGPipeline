from sentence_transformers import SentenceTransformer
from typing import List

class LocalEmbeddings:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        # Filter out empty strings
        documents = [doc for doc in documents if doc.strip()]

        # Check if the list is empty after filtering
        if not documents:
            raise ValueError("No non-empty documents to embed.")

        return self.model.encode(documents).tolist()

    def embed_query(self, query: str) -> List[float]:
        return self.model.encode([query])[0].tolist()
