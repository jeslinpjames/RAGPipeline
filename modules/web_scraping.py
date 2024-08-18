import requests
from bs4 import BeautifulSoup
from langchain.schema.document import Document
import uuid
from typing import List

def scrape_website(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract text from the website
    texts = soup.get_text(separator=' ', strip=True)
    
    return texts

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    # Split the text into chunks
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def add_website_to_vector_store(url: str, retriever, store):
    # Scrape the website
    website_text = scrape_website(url)
    
    # Chunk the text
    text_chunks = chunk_text(website_text)
    
    # Add to vector store
    doc_ids = [str(uuid.uuid4()) for _ in text_chunks]
    documents = [Document(page_content=chunk, metadata={"doc_id": doc_id}) for chunk, doc_id in zip(text_chunks, doc_ids)]
    
    retriever.vectorstore.add_documents(documents)
    store.mset(list(zip(doc_ids, text_chunks)))
