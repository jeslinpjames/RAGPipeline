import requests
from bs4 import BeautifulSoup
from langchain.schema.document import Document
import uuid
from typing import List, Tuple

def scrape_website(url: str) -> Tuple[str, List[str]]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract all the text from the website
    texts = soup.get_text(separator=' ', strip=True)
    
    # Extract tables
    tables = []
    for table in soup.find_all('table'):
        table_text = '\n'.join([' '.join(row.stripped_strings) for row in table.find_all('tr')])
        tables.append(table_text)
    
    return texts, tables

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
    website_text, tables = scrape_website(url)
    
    # Chunk the text and tables
    text_chunks = chunk_text(website_text)
    table_chunks = [chunk_text(table) for table in tables]
    table_chunks = [item for sublist in table_chunks for item in sublist]  # Flatten the list
    
    # Add text chunks to vector store
    doc_ids = [str(uuid.uuid4()) for _ in text_chunks]
    documents = [Document(page_content=chunk, metadata={"doc_id": doc_id}) for chunk, doc_id in zip(text_chunks, doc_ids)]
    
    retriever.vectorstore.add_documents(documents)
    store.mset(list(zip(doc_ids, text_chunks)))
    
    # Add table chunks to vector store
    table_ids = [str(uuid.uuid4()) for _ in table_chunks]
    table_documents = [Document(page_content=chunk, metadata={"doc_id": table_id}) for chunk, table_id in zip(table_chunks, table_ids)]
    
    retriever.vectorstore.add_documents(table_documents)
    store.mset(list(zip(table_ids, table_chunks)))
