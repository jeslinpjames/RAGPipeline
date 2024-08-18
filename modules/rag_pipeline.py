from langchain.prompts import ChatPromptTemplate
from langchain.schema.document import Document
from modules.llm_interface import send_prompt

def run_rag_pipeline(question: str, retriever) -> str:
    # Step 1: Retrieve documents related to the question
    docs = retriever.get_relevant_documents(question)
    
    # Step 2: Check if any documents were retrieved
    if not docs:
        return "No relevant documents found for the question."
    
    # Step 3: Prepare context from the retrieved documents
    if isinstance(docs[0], Document):
        context = "\n".join([doc.page_content for doc in docs])
    else:
        context = "\n".join(docs)
    
    # Step 4: Prepare the prompt
    template = """Answer the question based only on the following context, which can include text and tables:
    {context}
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    formatted_prompt = prompt.format(context=context, question=question)
    
    # Step 5: Send the prompt to Llama 3.1 and get the response
    response = send_prompt(formatted_prompt)
    
    # Step 6: Return the response, if available
    if response:
        return response.strip()
    else:
        return "No response from the model."
