# Import necessary modules
from modules.data_processing import load_and_partition_pdf
from modules.vector_store import initialize_vector_store, add_documents_to_vector_store
from modules.llm_interface import send_prompt
from modules.rag_pipeline import run_rag_pipeline

# 1. Load and process the PDF
pdf_filename = "PDFs/infosys-esg-report-2022-23.pdf"  # Replace with your PDF file name
table_elements, text_elements = load_and_partition_pdf(pdf_filename)

# 2. Summarize the table elements only
def summarize_element(element):
    prompt_template = "You are an assistant tasked with summarizing tables and text. \
    Give a concise summary of the table or text. Table or text chunk: {element}"
    prompt = prompt_template.format(element=element)
    response = send_prompt(prompt)
    return response

def batch_summarize_tables(elements):
    summaries = []
    for element in elements:
        summary = summarize_element(element)
        summaries.append(summary)
    return summaries

# Summarize only tables
table_summaries = batch_summarize_tables([e.text for e in table_elements])

# 3. Initialize the vector store and add the documents
retriever, store = initialize_vector_store()

# Add the documents to the vector store, without summarizing text elements
add_documents_to_vector_store(
    retriever, 
    store, 
    [e.text for e in text_elements],  # Original text elements, without summarization
    [e.text for e in table_elements],  # Original table elements
    text_summaries=[e.text for e in text_elements],  # Use original text instead of summaries
    table_summaries=table_summaries  # Use summarized tables
)

# 4. Ask a question and pass the retriever to the pipeline
question = "What is silhouette?"
answer = run_rag_pipeline(question, retriever)

# 5. Print the answer
print("Answer:", answer)
