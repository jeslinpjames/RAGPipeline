import uuid
from langchain_community.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain.retrievers.multi_vector import MultiVectorRetriever
from modules.embedding import LocalEmbeddings  # Adjust import path as needed

def initialize_vector_store() -> (MultiVectorRetriever, InMemoryStore):
    embedding_function = LocalEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = Chroma(
        collection_name="summaries",
        embedding_function=embedding_function
    )

    store = InMemoryStore()
    id_key = "doc_id"

    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=store,
        id_key=id_key,
    )
    
    return retriever, store

def add_documents_to_vector_store(retriever, store, texts, tables, text_summaries, table_summaries):
    id_key = retriever.id_key  # Ensure you use the correct key

    # Add texts if not empty
    if texts:
        doc_ids = [str(uuid.uuid4()) for _ in texts]
        summary_texts = [Document(page_content=s, metadata={id_key: doc_ids[i]}) for i, s in enumerate(text_summaries)]
        retriever.vectorstore.add_documents(summary_texts)
        retriever.docstore.mset(list(zip(doc_ids, texts)))

    # Add tables if not empty
    if tables:
        table_ids = [str(uuid.uuid4()) for _ in tables]
        summary_tables = [Document(page_content=s, metadata={id_key: table_ids[i]}) for i, s in enumerate(table_summaries)]
        retriever.vectorstore.add_documents(summary_tables)
        retriever.docstore.mset(list(zip(table_ids, tables)))
